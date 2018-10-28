from django.shortcuts import render


from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from rest_framework.views import APIView
import requests
import pandas as pd

# Create your views here.

filePath = "word_search.tsv"

def index_page(request):
    return render(request, 'index.html')


class search(APIView):
    def get(self, request):
        # Get the word to search from the url
        item = request.GET['word']

        # Read .tsv file to a pandas dataframe
        datadf = pd.read_table(filePath,
                             delim_whitespace=True, names=["words", "frequency"])

        # filtering out all the matching words from the dataframe and adding it to a new dataframe
        filteredDatadf = datadf[datadf['words'].str.contains(item, na=False)]

        # sorting the filtered data by its frequency
        filteredDatadf = filteredDatadf.sort_values(by=['frequency'], ascending=False)

        # further filtering it on lenght of the words matched
        filteredDatadf_index1 = filteredDatadf.words.str.len().sort_values().index

        # reindexing the dataframe by the indexes found above
        filteredDatadf1 = filteredDatadf.reindex(filteredDatadf_index1).head(25)


        # getting all the words stating from the serached word and reindexing the dataframe
        filteredDatadf_index2 = filteredDatadf1[filteredDatadf1.words.str.startswith(item)].index
        filteredDatadf2 = filteredDatadf1.reindex(filteredDatadf_index2).head(25)

        # converting dataframe to json
        filteredData_json1 = filteredDatadf1.to_dict('records')
        filteredData_json2 = filteredDatadf2.to_dict('records')

        # checking for unique values and merging two json
        finalfilteredData_json = []
        for i in filteredData_json1:
            temp = []
            for j in filteredData_json2:
                if i['words'] in j['words']:
                    temp.append("true")
                else:
                    temp.append("false")
            if 'true' not in temp:
                finalfilteredData_json.append(i)
        for i in finalfilteredData_json:
            filteredData_json2.append(i)
        return JsonResponse(filteredData_json2, safe=False)
