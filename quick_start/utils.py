import pandas as pd
import PySimpleGUI as sg

from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.resource import ResourceManagementClient
import os

def list_oai_models(subscription_id:str, resource_group:str, cognitive_service_name:str) -> pd.DataFrame:
    """
        Input parameters are subscription_id, resource_group, cognitive_service_name and returns a pandas DataFrame

        subscription_id: the subscription id that has a deploy Azure OpenAI instance
        resource_group:  the reource group name that is hosting the cognitive service
        cognitive_service_name: name of the Azure OpenAI service name
    """
    client = CognitiveServicesManagementClient(credential=DefaultAzureCredential(), subscription_id=subscription_id)
    models = client.deployments.list(resource_group,cognitive_service_name)

    aoai_df = pd.DataFrame(columns=["display_name","format","model","version","call_rate_limit"])

    for model in models:
        aoai_df = pd.concat([aoai_df, pd.DataFrame([
        {"display_name": model.name, 
        "format": model.properties.model.format, 
        "model": model.properties.model.name, 
        "version": model.properties.model.version, 
        "call_rate_limit": model.properties.model.call_rate_limit}])], ignore_index=True)

    return aoai_df


def popup_choice():
    sg.theme('Dark Grey 9')   # Add a touch of color

    df = list_oai_models(os.getenv("mysubscription"), "coding-forge", "codingforgeai")

    options = df['display_name'].values

    # All the stuff inside your window.
    layout = [ 
                [
                    sg.Text(size=(30,5),text='Select one of the available \nmodels', text_color="Green", font=("Arial",22)), 
                    sg.Listbox(options,select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,size=(80,len(options)), font=("Helvetica",25))],
                [   sg.Button('Ok'), sg.Button('Cancel')]
            ]

    # Create the Window
    window = sg.Window('Make your choice', layout)

    # Event Loop to process "events" and get the "values" of the input
    while True:
        event, values = window.read()
        print( f"event={event}" )
        if event is None or event == 'Ok' or event == 'Cancel': # if user closes window or clicks cancel
            break
            
    # close  the window        
    window.close()

    if event == "Cancel":
        print( "You cancelled" )
    else:
        if type(values[0]) is list:
            return values[0][0]
        else:
            return values[0]
        #print('You entered ', values[0])
        #sg.popup( f"You selected {values[0]}" )