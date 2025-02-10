from PyQt6.QtWidgets import QApplication
from app.windows.authentication_widow import LoginApplicationGUI

def main():
	import sys
	app = QApplication(sys.argv)
	gui = LoginApplicationGUI()
	gui.show()

	try:
		sys.exit(app.exec())
	except SystemExit:
		print('Close...')

if __name__ == '__main__':
  	main()