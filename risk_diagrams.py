import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from get_data_brasil import run_crear_excel_brasil
from get_data_brasil_wcota import run_crear_excel_brasil_wcota
from get_data_pernambuco import run_crear_excel_recife
from get_data_ourworldindata import run_crear_excel_ourworldindata
from pandas import ExcelWriter
import colormap
import plotly.graph_objects as go
from PIL import Image
import base64
import os

matplotlib.use('tkagg')


def run_risk_diagrams(argv_1, deaths, file_others_cases, file_others_pop, radio_valor, ourworldindata_country):

    if argv_1:
        last_days_time = 30
        brasil = False
        pt = False
        html = False
        last_days = False
        animation = False

        if radio_valor == 1:
            last_days = True
        elif radio_valor == 2:
            html = True
        else:
            pass

        dataTable = []
        dataTable_EPG = []

        if argv_1 == 'recife':
            try:
                run_crear_excel_recife()
                filename = 'data/cases-recife.xlsx'
                filename_population = 'data/pop_recife_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')
        
        elif argv_1 == 'rain':
            try:
                filename = 'data/rain.json'
            except AttributeError:
                print('Error! Not found file or could not download!')

        data = pd.read_json(filename)
    
        for ID in data.keys():
            preciptation = np.zeros((len(data[ID])), dtype=np.float)
            tide = np.zeros((len(data[ID])), dtype=np.float)
            tim = np.zeros((len(data[ID])), dtype=np.str)
            for i in range(len(data[ID])):
                preciptation[i] = data[ID][i]['preciptation']
                tide[i] = data[ID][i]['tide']
                tim[i] = data[ID][i]['time']

            first_time = data[ID][0]['time']
            last_time = data[ID][len(data[ID]) - 1]['time']
            last_day = data[ID][len(data[ID]) - 1]['date']
        
            # For last 15 days
            # if last_days:
            #     a_14_days_solo = []
            #     day13 = len(a_14_days) - last_days_time
            #     first_day = dia[day13]
            #     for i in range(len(a_14_days)):
            #         if i >= len(a_14_days) - last_days_time:
            #             a_14_days_solo.append(a_14_days[i])
            #         else:
            #             a_14_days_solo.append(None)

            last_day =last_day.replace('/', '-')
            save_path = 'static_graphic' + '/' + last_day + '-' + data[ID].name
            save_path_temp = 'static_graphic' + '/interactive_graphic/' + last_day + '-' + data[ID].name
            save_path_xlsx = 'static_graphic/xlsx/'

            fig1, ax1 = plt.subplots(sharex=True)
            if last_days:
                # ax1.plot(a_14_days,  p_seven, 'ko--', fillstyle='none',
                #          linewidth=0.5, color=(0, 0, 0, 0.15))
                # ax1.plot(a_14_days_solo,  p_seven, 'ko--',
                #          fillstyle='none', linewidth=0.5)  # For last 15 days
                # ax1.plot(a_14_days_solo[len(a_14_days_solo) - 1],
                #          p_seven[len(p_seven) - 1], 'bo')
                pass
            else:
                ax1.plot(preciptation,  tide, 'ko--',
                         fillstyle='none', linewidth=0.5)
                ax1.plot(preciptation[len(preciptation) - 1],
                         tide[len(tide) - 1], 'bo')
            lim = ax1.get_xlim()
            x = np.ones(int(lim[1]))
            ax1.plot(x, 'k--', fillstyle='none', linewidth=0.5)
            ax1.set_ylim(0, 5)
            
            ax1.set_xlim(0, int(lim[1]))

            ax1.set_ylabel('Tidal highness (meters)')
            ax1.set_xlabel('Preciptation (mm/h)')
            ax1.annotate(first_time,
                         xy=(preciptation[0], tide[0]
                             ), xycoords='data',
                         xytext=(len(x) - abs(len(x) / 1.5), 2.7), textcoords='data',
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="arc3", linewidth=0.4),
                         )
            ax1.annotate(last_time,
                         xy=(preciptation[len(preciptation) - 1],
                             tide[len(tide) - 1]), xycoords='data',
                         xytext=(len(x) - abs(len(x) / 2), 3), textcoords='data',
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="arc3", linewidth=0.4),
                         )

           
            # bra_title = data[ID]
            plt.title(data[ID].name)
            plt.annotate(
                ' EPG > 50: High', xy=(len(x) - abs(len(x) / 3.5), 4.8), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
            plt.annotate(
                " 25,1 < EPG < 50 : Moderate", xy=(len(x) - abs(len(x) / 3.5), 4.55), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
            plt.annotate(
                ' EPG < 25: Low', xy=(len(x) - abs(len(x) / 3.5), 4.3), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))

            plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 4.8), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(1, 0, 0, .5), lw=0, pad=2))
            plt.annotate(
                "  \n", xy=(len(x) - abs(len(x) / 3.3), 4.55), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(1, 1, 0, .5), lw=0, pad=2))
            plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 4.3), color=(0, 0, 0),
                ha='left', va='center', fontsize='6',
                bbox=dict(fc=(0, 1, 0, .5), lw=0, pad=2))

            rh = np.arange(0, int(lim[1]), 1)
            ar = np.linspace(0, 4, 400)

            RH, AR = np.meshgrid(rh, ar)

            EPG = RH * AR

            for i in range(len(EPG)):
                for j in range(len(EPG[i])):
                    if EPG[i][j] > 50:
                        EPG[i][j] = 50
            c = colormap.Colormap()
            mycmap = c.cmap_linear('green(w3c)', 'yellow', 'red')
            ax1.pcolorfast([0, int(lim[1])], [0, 5],
                           EPG, cmap=mycmap, alpha=0.6)

            ax1.set_aspect('auto')

            if html:
                # figt, axt = plt.subplots(sharex=True)
                # axt.pcolorfast([0, int(lim[1])], [0, 4],
                #                EPG, cmap=mycmap, alpha=0.6)
                # axt.set_axis_off()
                # figt.savefig(save_path_temp, format='png',
                #              bbox_inches='tight', dpi=300, pad_inches=0)
                # plotly_html(a_14_days, p_seven, dia, bra_title,
                #             save_path_xlsx, save_path_temp)
                pass
            else:
                plt.savefig(save_path + '.png', bbox_inches='tight', dpi=300)
                plt.close('all')
            print(
                "\n\nPrediction for the region of " + data[ID].name + " performed successfully!\nPath:" + save_path)

    

            # dataTable.append([region[ID], cumulative_cases[len(cumulative_cases) - 1], new_cases[len(new_cases) - 1], p[len(p) - 1], p_seven[len(
            #     p_seven) - 1], n_14_days[len(n_14_days) - 1], a_14_days[len(a_14_days) - 1], risk[len(risk) - 1], risk_per_10[len(risk_per_10) - 1]])

            # for i in range(len(dia)):
            #     dataTable_EPG.append([dia[i], region[ID], risk_per_10[i]])

    # df = pd.DataFrame(dataTable, columns=['State', 'Cumulative cases', 'New cases', 'ρ', 'ρ7', 'New cases last 14 days (N14)',
    #                                       'New cases last 14 days per 105 inhabitants (A14)', 'Risk (N14*ρ7)',  'Risk per 10^5 (A14*ρ7)'])
    # df_EPG = pd.DataFrame(dataTable_EPG, columns=['DATE', 'CITY', 'EPG'])

    # with ExcelWriter(save_path_xlsx + last_day + '_' + argv_1 + '_report.xlsx') as writer:
    #     df.to_excel(writer, sheet_name='Alt_Urgell')
    # with ExcelWriter(save_path_xlsx + last_day + '_' + argv_1 + '_report_EPG.xlsx') as writer:
    #     df_EPG.to_excel(writer, sheet_name='Alt_Urgell')
