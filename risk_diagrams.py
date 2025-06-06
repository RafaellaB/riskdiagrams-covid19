import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import colormap

matplotlib.use('tkagg')


def run_risk_diagrams(argv_1, radio_valor):

    if argv_1:
        last_days_time = 30
        html = False
        last_days = False

        if radio_valor == 1:
            last_days = True
        elif radio_valor == 2:
            html = True
        else:
            pass
        
        if argv_1 == 'rain':
            try:
                filename = 'data/rain.json'
            except AttributeError:
                print('Error! File not found or could not download!')

        data = pd.read_json(filename)
    
        for ID in data.keys():
            preciptation = np.zeros((len(data[ID])), dtype=float)
            tide = np.zeros((len(data[ID])), dtype=float)
            time = np.zeros((len(data[ID])), dtype=str)
            for i in range(len(data[ID])):
                preciptation[i] = data[ID][i]['preciptation']
                tide[i] = data[ID][i]['tide']
                time[i] = data[ID][i]['time']

            first_time = data[ID][0]['time']
            last_time = data[ID][len(data[ID]) - 1]['time']
            last_day = data[ID][len(data[ID]) - 1]['date']

            last_day = last_day.replace('/', '-')
            save_path = 'static_graphic' + '/' + last_day + '-' + data[ID].name
            save_path_interactive = 'static_graphic' + '/interactive_graphic/' + last_day + '-' + data[ID].name

            fig1, ax1 = plt.subplots(sharex=True)
            
            # TODO: For last X days
            if last_days:
                """
                This model came from Covid risk diagram
                """
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

            # TODO: Work on thois for interactive graphics
            if html:
                """
                This model came from Covid risk diagram
                """
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
