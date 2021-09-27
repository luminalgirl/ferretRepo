import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QLabel

file1 = ""
file2 = ""
directory = ""
class MyApp(QWidget):
	def __init__(self):
		super().__init__()
		self.window_width, self.window_height = 800, 200
		self.setMinimumSize(self.window_width, self.window_height)

		layout = QVBoxLayout()
		self.setLayout(layout)
		btn1 = QPushButton('Ruta del archivo PDF a dividir')
		btn1.clicked.connect(self.getFileNamePDF)
		layout.addWidget(btn1)
		label1 = QLabel("Archvo PDF...")
		layout.addWidget(label1)


		btn2 = QPushButton('Ruta del archivo TXT con nombres')
		btn2.clicked.connect(self.getFileNameTXT)
		layout.addWidget(btn2)
		label2 = QLabel("Archvo TXT...")
		layout.addWidget(label2)

		btn3 = QPushButton('Ruta destino de los archivos')
		btn3.clicked.connect(self.getDirectory)
		layout.addWidget(btn3)
		label3 = QLabel("Folder destino...")
		layout.addWidget(label3)       
		
		self.label1 = label1
		self.label2 = label2
		self.label3 = label3

		

		btn = QPushButton('Dividir')
		btn.clicked.connect(self.launchDialog)
		layout.addWidget(btn)
	def sendError(self,mensaje):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText("Error")
		msg.setInformativeText(mensaje)
		msg.setWindowTitle("Error")
		msg.exec_()

	def launchDialog(self):
		
		if file1=="" or file2=="" or directory=="":
			self.sendError('Ingresa todos las rutas solicitadas')	
		else:
			inputpdf = PdfFileReader(open(file1, "rb"))
			filenames = []
			with open(file2,'r') as f:
				for line in f.readlines():
					l = line.strip()
					if l!="" and l != None:
						filenames.append(l)
			print(filenames)
			if inputpdf.numPages != len(filenames):
				self.sendError('El numero de páginas y de nombres no coincide.')
				return None
			for i in range(inputpdf.numPages):
				output = PdfFileWriter()
				output.addPage(inputpdf.getPage(i))
				filename = directory+"/"+filenames[i]+".pdf" 
				print(filename)
				with open(filename, "wb") as outputStream:
					output.write(outputStream)
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Finalizado")
			msg.setInformativeText('El archivo ha sido dividido con éxito')
			msg.setWindowTitle("Finalizado")
			msg.exec_()
	
	def getFileNamePDF(self):
		global file1
		response = QFileDialog.getOpenFileName(
			parent=self,
			caption='Selecciona un archivo',
			directory=os.getcwd(),        

		)
		print(response)
		file1 = response[0]
		self.label1.setText(response[0])
		return response[0]
	
	def getFileNameTXT(self):
		global file2
		response = QFileDialog.getOpenFileName(
			parent=self,
			caption='Selecciona un archivo',
			directory=os.getcwd(),        
		)
		print(response)     
		file2 = response[0]
		self.label2.setText(response[0])
		return response[0]

	def getDirectory(self):
		global directory
		response = QFileDialog.getExistingDirectory(
			self,
			caption='Selecciona un directorio'
		)
		print(response)
		directory = response
		self.label3.setText(response)
		return response     

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			
		}
	''')
	
	myApp = MyApp()
	myApp.show()    
	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')