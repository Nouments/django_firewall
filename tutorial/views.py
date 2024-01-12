from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import subprocess
from django.template import loader
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status

def icmp(allowed_ip,target,chaine,act):
    try:
        # Autoriser le trafic ICMP (ping) depuis l'adresse IP spécifiée
        subprocess.run(['sudo', 'iptables', act, chaine, '-p', 'icmp', '-s', allowed_ip, '-j', 'DROP'], check=True)
        print(f"Règle ajoutée pour autoriser le trafic ICMP depuis {allowed_ip}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ajout de la règle : {e.stderr}")
        
        

def action(destination_ip,protocole,target,chaine,act,port):
    try:
        # Bloquer le trafic TCP sortant vers l'adresse IP spécifiée
        subprocess.run(['sudo', 'iptables', act, chaine, '-p', protocole, '--dp', port, '-d', destination_ip, '-j', target], check=True)
        print(f"Règle ajoutée pour bloquer le trafic TCP sortant vers {destination_ip}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ajout de la règle : {e.stderr}")



def convert_to_serializable(obj):
    """Convert non-serializable objects to serializable ones."""
    if isinstance(obj, subprocess.CompletedProcess):
        return {
            'returncode': obj.returncode,
            'stdout': obj.stdout,
            'stderr': obj.stderr,
        }
    return obj
   
def list_rules(chain):
    try:
        result = subprocess.run(['iptables', '-L', chain], capture_output=True, text=True, check=True)
        
        # Créer une liste de dictionnaires pour stocker les informations des règles
        rules_list = []
        
        # Séparer les lignes de sortie en fonction des sauts de ligne
        output_lines = result.stdout.split('\n')
        
        # Ignorer la première ligne qui contient l'en-tête
        for line in output_lines[2:]:
            # Diviser la ligne en colonnes
            columns = line.split()
            
            # Vérifier si la ligne a des colonnes (évite les lignes vides)
            if columns:
                # Créer un dictionnaire pour stocker les informations de la règle
                rule_info = {
                    'chaine':chain,
                    'target': columns[0],
                    'prot': columns[1],
                    'opt': columns[2],
                    'source': columns[3],
                    'destination': columns[4]
                }
                
                # Ajouter le dictionnaire à la liste
                rules_list.append(rule_info)
        
        # Afficher la liste de dictionnaires
        return rules_list
        for rule in rules_list:
            print(rule)
            
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la commande iptables : {e.stderr}")

    a=list_rules('OUTPUT')
    b=list_rules('FORWARD')
    a.extend(b)
    for i in a:
        print(i)

def listes(request):
    a=list_rules('FORWARD')
    b=list_rules('OUTPUT')
    c=list_rules('INPUT')
    a.extend(b)
    a.extend(c)
    
    return JsonResponse(a, safe=False, json_dumps_params={'default': convert_to_serializable})

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def add(request):
    return  JsonResponse()

class ReceiveJSONDataView(APIView):
    @parser_classes([JSONParser])
    def post(self, request, *args, **kwargs):
        # Vérifier si le type de contenu est application/json
        if request.content_type != 'application/json':
            return Response({'error': 'Le type de contenu doit être application/json'}, status=status.HTTP_400_BAD_REQUEST)

        # Accéder aux données JSON à partir de la requête
        json_data = request.data
        ip = json_data['dest']
        chaine = json_data['chaine']
        act = json_data['act']
        protocol = json_data['protocol']
        targ = json_data['target']
        port = json_data['port']
        
        if port=='':
            icmp(ip,targ,chaine,act)
        else:
            action(ip,protocol,targ,chaine,act,port)
            
        # Faire quelque chose avec les données JSON, par exemple, les imprimer
        print("Données JSON reçues :", json_data['protocol'])

        # Répondre avec un message JSON
        response_data = {'message': 'Données JSON reçues avec succès'}
        return Response(response_data, status=status.HTTP_200_OK)
