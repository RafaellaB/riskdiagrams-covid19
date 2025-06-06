from risk_diagrams import run_risk_diagrams
import sys

if __name__ == "__main__":

    #radio_valor =  0 None | 1 last_days | 2 html 
    radio_valor = 0
    run_risk_diagrams('rain', radio_valor)

    sys.exit()
