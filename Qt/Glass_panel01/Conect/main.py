
from __future__ import print_function

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import logging

from array import *
arrayManualMode = array('b', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
arrayManualModePower = array('f', [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

# ----------------------------------------------------------------------------------------------------------

# функция обработки записи по TCP данных в PLC
def main():
    """main"""
    logger = modbus_tk.utils.create_logger("console", level=logging.DEBUG)

    def on_after_recv(data):
        master, bytes_data = data
        logger.info(bytes_data)

    hooks.install_hook('modbus.Master.after_recv', on_after_recv)

    try:
        def on_before_connect(args):
            master = args[0]
            logger.debug("on_before_connect {0} {1}".format(master._host, master._port))

        hooks.install_hook("modbus_tcp.TcpMaster.before_connect", on_before_connect)

        def on_after_recv(args):
            response = args[1]
            logger.debug("on_after_recv {0} bytes received".format(len(response)))

        hooks.install_hook("modbus_tcp.TcpMaster.after_recv", on_after_recv)

        # Connect to the slave
        master = modbus_tcp.TcpMaster(host='10.0.0.1', port=502)
        master.set_timeout(5.0)
        logger.info("connected")

        # master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 10)
        # master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=4096, output_value=arrayManualModePower[0], data_format='>f')
        # master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=4098, output_value=arrayManualModePower[1], data_format='>f')
        # master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=4100, output_value=arrayManualModePower[2], data_format='>f')
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 4096, output_value=arrayManualModePower[0])
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 4097, output_value=arrayManualModePower[1])
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 4098, output_value=arrayManualModePower[2])
        master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=arrayManualMode)
        print(arrayManualMode)
        print(arrayManualModePower)
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2))  ##
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2, data_format='f'))

        # Read and write floats
        # master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, starting_address=0, output_value=[3.14], data_format='>f')
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2, data_format='>f'))

        # send some queries
        # logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        # logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))

        # self, slave, function_code, starting_address, quantity_of_x = 0, output_value = 0, data_format = "", expected_length = -1, write_starting_address_FC23 = 0):
        # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 16, 1))
        # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 4097, 1))

        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        # logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())




# ----------------------------------------------------------------------------------------------------------

# Здесь создаем окно оператора, в котором обрабатываем события  - в последствии нужно убрать в manualwindow
from Qt.test01 import *
import sys


# 0 - pushButton_PowerSystem        - fixed         - включение установки
# 1 - pushButton_plates_servo_left                  - вращение пластин
# 2 - pushButton_plates_servo_right                 - вращение пластин
# 3 - pushButton_plates_up          - fixed         - подьем пластин
# 4 - pushButton_mixer_turn         - fixed         - поворот мишалки
# 5 - pushButton_mixer_up           - fixed         - подьем мишалки
# 6 - pushButton_mixer_on           - fixed         - включение мишалки
# 7 - pushButton_handPlate_takeGive - fixed         - включение ардуино
#


#класс обработки действий на панеле оператора
class mywindow (QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_mainWindow()                                                           #отвечающие за загрузку сгенерированного класса python из файла пользовательского интерфейса:
        self.ui.setupUi(self)


        self.ui.pushButton_PowerSystem.setCheckable(True)                                   #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_PowerSystem.clicked.connect(self.mymain)                         #запускает функцию в момент отжатия


        self.ui.pushButton_plates_servo_left.pressed.connect(self.mymain)                   #проверяет в момент нажатия
        self.ui.pushButton_plates_servo_left.clicked.connect(self.mymain)                   #проверяет в момент отжатия
        self.ui.pushButton_plates_servo_right.pressed.connect(self.mymain)                  #проверяет в момент нажатия
        self.ui.pushButton_plates_servo_right.clicked.connect(self.mymain)                  #проверяет в момент отжатия

        self.ui.pushButton_plates_up.setCheckable(True)                                     #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_plates_up.clicked.connect(self.mymain)

        self.ui.pushButton_mixer_turn.setCheckable(True)                                    #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_mixer_turn.clicked.connect(self.mymain)
        self.ui.pushButton_mixer_up.setCheckable(True)                                      #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_mixer_up.clicked.connect(self.mymain)
        self.ui.pushButton_mixer_on.setCheckable(True)                                      #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_mixer_on.clicked.connect(self.mymain)
        self.ui.pushButton_handPlate_takeGive.setCheckable(True)                            #Распознает нажатые и отпущенные состояния кнопки, если установлено значение true
        self.ui.pushButton_handPlate_takeGive.clicked.connect(self.mymain)

        self.ui.doubleSpinBox_Volt.valueChanged.connect(self.volt)
        self.ui.doubleSpinBox_Current.valueChanged.connect(self.curr)
        self.ui.doubleSpinBox_TimeWorkPower.valueChanged.connect(self.timePow)

    def volt(self):
        arrayManualModePower[0] = float(self.ui.doubleSpinBox_Volt.value())
        # print(arrayManualModePower[0])
        main()
    def curr(self):
        arrayManualModePower[1] = float(self.ui.doubleSpinBox_Current.value())
        # print(arrayManualModePower[1])
        main()
    def timePow(self):
        arrayManualModePower[2] = float(self.ui.doubleSpinBox_TimeWorkPower.value())
        # print(arrayManualModePower[2])
        main()

    def valuechange(self):
        self.ui.label.setText("current value:" + str(self.ui.doubleSpinBox.value()))

    def mymain(self):
        arrayManualMode[0] = self.ui.pushButton_PowerSystem.isChecked()
        arrayManualMode[1] = self.ui.pushButton_plates_servo_left.isDown()
        arrayManualMode[2] = self.ui.pushButton_plates_servo_right.isDown()
        arrayManualMode[3] = self.ui.pushButton_plates_up.isChecked()
        arrayManualMode[4] = self.ui.pushButton_mixer_turn.isChecked()
        arrayManualMode[5] = self.ui.pushButton_mixer_up.isChecked()
        arrayManualMode[6] = self.ui.pushButton_mixer_on.isChecked()
        arrayManualMode[7] = self.ui.pushButton_handPlate_takeGive.isChecked()

        main()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
if __name__ == "__main__":
    main()
sys.exit(app.exec())

