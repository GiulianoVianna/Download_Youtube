from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import  QTimer, QTime
from PyQt5.uic import loadUi
from mhyt import yt_download
from threading import *
from PyQt5.QtWidgets import QMessageBox

### Importando tela do do arquivo youtube.py 

from youtube import Ui_Form

count = 0
minutos = 0
segundos = 0
regra = 0
tempo = 0

### Classe Tela Principal ###

class youtube(QMainWindow):

    def __init__(self, *args, **argvs):
        super(youtube, self).__init__(*args, **argvs)
        self.ui = Ui_Form()
        self.ui.setupUi(self) 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.lcd_time)        
        self.timer.start(1000)
        self.ui.bt_download.clicked.connect(self.thread)

###########################################################################

    # Funções - Mensagem     

    def mensagem_link(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção!')
        msg1.setText('Favor informar um Link!')
        x = msg1.exec()
    
    def mensagem_nome_arquivo(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção!')
        msg1.setText('Favor informar um nome para a música!')
        x = msg1.exec()

    def mensagem_link_error(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção!')
        msg1.setText('Favor informar um Link válido!')
        x = msg1.exec()

###########################################################################


   ### Função lcd_time - Atualiza display e o tempo de download
    def lcd_time(self):

        global count, minutos, segundos, regra, tempo
        
        tempo_corrente = QTime.currentTime()
        display = tempo_corrente.toString('hh:mm:ss')
        self.ui.lcdNumber.display(display) 

        # Timer do tempo de download 
        if regra == 1:
            if count < 60:
                count += 1
                segundos = count            

            else:
                minutos += 1
                segundos = 0
                count = 0

            tempo = f'Tempo: {minutos}:{segundos}'
            self.ui.lb_download.setText(tempo)

###########################################################################

    # Função para o processo não travar - Thread
    def thread(self):

        if self.ui.txt_link.text() == "":               

            self.mensagem_link()
            self.ui.txt_link.setFocus()

        elif self.ui.txt_nome.text() == "":

            self.mensagem_nome_arquivo()
            self.ui.txt_nome.setFocus()
        
        else:

            t1=Thread(target=self.download)
            t1.start()


###########################################################################
            
    # Função - Download do youtube

    def download(self):
        
        global regra, count, minutos, segundos, tempo

        self.ui.lb_download.setText("Tempo: 00:00")
        self.ui.lb_download.setStyleSheet("color: rgb(0, 85, 255);")        

        count = 0
        minutos = 0
        segundos = 0

        try:                 

            regra = 1  # Atribuição de valor para iniciar o timer - tempo de download
            print(regra)

            if self.ui.rb_mp4.isChecked() == True:
                url = self.ui.txt_link.text()
                self.titulo = self.ui.txt_nome.text()
                self.titulo_mp4 = self.titulo + '.mp4'
                yt_download(url, self.titulo_mp4)  # Converte arquivo em .mp4

            elif self.ui.rb_mp3.isChecked() == True:
                url = self.ui.txt_link.text()
                self.titulo = self.ui.txt_nome.text()
                self.titulo_mp3 = self.titulo + '.mp3' 
                yt_download(url, self.titulo_mp3, ismusic=True, codec='mp3')  # Converte arquivo em .mp3

            regra = 0  # Atribuição de valor pausa o timer do tempo de download
            print(regra)
            self.ui.lb_download.setText(f'Finalizado - {tempo}')
            self.ui.lb_download.setStyleSheet("color: rgb(0, 85, 0);")

        except:
            self.mensagem_link_error()
            regra = 0  

###########################################################################

app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    windows = youtube()
    windows.show()

sys.exit(app.exec_())