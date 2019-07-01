import pandas as pd

import os
from StyleFrame import StyleFrame, Styler

from PyQt5 import QtWidgets

class BattleInfoSpreadsheet(object):
    '''Creates and populates an excel spreadsheet to keep track
       of relevant information for DnD battles, such as initiative,
       whose turn it is, allegiance of characters, and health status
       of character
    '''

    def __init__(self, battle_object, spreadsheet_name, file_name):


        self.battle_object = battle_object
        # Organize creature list into pandas dataframe

        self.spreadsheet_name = spreadsheet_name

        self.file_name = file_name

        self.color_code =  {
                "Player": 'background-color: blue',
                "Ally": 'background-color: green',
                "Neutral": 'background-color: pink',
                "Foe": 'background-color: red',
                "Dead": 'background-color: black'
                           }


    def create_pd_dataframe(self, ordered_creature_list, stylized=False):

        columns = ["Name", "Type", "NPC?", "Allegiance", "HP", "Initiative"]
        data = []
        ordered_creature_tuples = []
        for creature in ordered_creature_list:
            if creature.npc == 1:
                is_npc = "NPC"
            else:
                is_npc = "Player"
            creature_data = [creature.name, creature.creature_type,
                    is_npc, creature.allegiance, creature.hp, 
                    creature.initiative]
            data.append(creature_data)

        battle_df = pd.DataFrame(data,columns=columns)

        if stylized:
            player_list = self.battle_object.player_list
            foe_list = self.battle_object.foe_list
            neutral_list = self.battle_object.neutral_list
            allied_list = self.battle_object.allied_list

            for player in player_list: 
                battle_df.loc[player,:] = self.color_code["Player"]
            for foe in foe_list:
                battle_df.loc[foe,:] = self.color_code["Foe"]
            for neutral in neutral_list
                battle_df.loc[neutral,:] = self.color_code["Neutral"]
            for ally in allied_list:
                battle_df.loc[ally,:] = self.color_code["Ally"]

            # Check for dead creatures
            for creature in orderedCreatureList:
                if creature.dead:
                    battle_df.loc[ally,:] = self.color_code["Dead"]

        return battle_df


    def fill_basic_excel_spreadsheet(self, battle_df, file_name):

        if not file_name.endswith('.xlsx'): 
            file_name = file_name + '.xlsx'
        battle_df.to_excel(file_name)
        self.file_name = file_name

    def fill_advanced_excel_spreadsheet(self, battle_df, file_name,
                    sheet_name, save_path):

        if not file_name.endswith('.xlsx'): 
            file_name = file_name + '.xlsx'

        # Check if the excel workbook with name 'file_name' has
        # already been created
        file_path = os.path.join(save_path, file_name)
        if os.path.exists(file_path)

        else:
            # Stylize pandas dataframe
            


            writer = pd.ExcelWriter(file_name, engine='xlsxwriter',
                                    sheet_name)

            battle_df.to_excel(writer, sheet_name=sheet_name)
            workbook = writer.bookworksheet = writer.sheets[sheet_name]

    def display_spreadsheet_in_gui(self, battle_df):
        '''displays battle dataframe'''
        win = QtWidgets.QWidget()
        scroll = QtWidgets.QScrollArea()
        layout = QtWidgets.QVBoxLayout()
        table = QtWidgets.QTableWidget()
        scroll.setWidget(table)
        layout.addWidget(table)
        win.setLayout(layout)

        table.setColumnCount(len(df.index))
        table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

        return win








