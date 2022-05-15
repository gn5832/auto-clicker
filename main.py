import threading
from time import sleep
import keyboard, mouse



class ClickerPrinter:
    MODULE_NAME = 'Clicker'

    def _str_to_print_format(self, string):
        return f'{ClickerPrinter.MODULE_NAME} | {string}'
        
    def custom_print(self, string):
        print(self._str_to_print_format(string))

    def custom_input(self, string):
        return input(self._str_to_print_format(string))


class ClickerSettingsCollector:
    LEFT_OPTIONS = ('l', 'L', '1', '')
    LEFT_CLICK = 'left'
    RIGHT_CLICK = 'right'

    START_HOTKEY = 'Ctrl + 1'
    TOGGLE_MOUSE_HOTKEY = 'Ctrl + 2'

    def __init__(self):
        self._printer = ClickerPrinter()
        self._set_delay()
        self._set_mouse_btn()
        self._print_start_text()

    def _set_delay(self):
        raw_delay = self._printer.custom_input('Укажите задержку в миллисекундах: ')
        if not raw_delay: raw_delay = 1
        self.delay = float(raw_delay) / 1000

    def _set_mouse_btn(self):
        raw_mouse_btn = self._printer.custom_input(f'Выберите кнопку мыши 1 или 2: ')
        self.mouse_btn = self.LEFT_CLICK if raw_mouse_btn.startswith(self.LEFT_OPTIONS) else self.RIGHT_CLICK

    def _print_start_text(self):
        print()
        self._printer.custom_print(f'Задержка перед кликом: {self.delay}сек. | Выбрана кнопка мыши: {self.mouse_btn}')
        self._printer.custom_print(f'Для запуска кликера нажмите: {self.START_HOTKEY}')
        self._printer.custom_print(f'Для смены кнопки мыши нажмите: {self.TOGGLE_MOUSE_HOTKEY}')


class Clicker(threading.Thread):
    _settings = ClickerSettingsCollector()
    _printer = ClickerPrinter()
    all_click_counter = 0
    is_run = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_counter = 0

    def run(self):
        while self.is_run:
            sleep(self._settings.delay)
            mouse.click(button=self._settings.mouse_btn)
            Clicker.all_click_counter += 1
            self.click_counter += 1
            if not self.click_counter % 10:
                print(self.click_counter, end='\r')

    @classmethod
    def start_clicker(cls):
        """Вкл/Выкл кликера."""
        if cls.run_switcher(): return
        clicker = Clicker(daemon=True)
        clicker.start()

    @classmethod
    def run_switcher(cls):
        cls.is_run = False if cls.is_run else True
        cls.print_change_run_state()
        return not cls.is_run

    @classmethod
    def print_change_run_state(cls):
        print()
        cls._printer.custom_print(f'Состояние запуска изменено: {cls.is_run}')
        if not cls.is_run:
            cls._printer.custom_print(f'Всего кликов сделано: {cls.all_click_counter} | Задержка: {cls._settings.delay}сек. | Кнопка: {cls._settings.mouse_btn}')

    @classmethod
    def toggle_mouse_btn(cls):
        if cls._settings.mouse_btn == cls._settings.LEFT_CLICK: 
            cls._settings.mouse_btn = cls._settings.RIGHT_CLICK
        else:
            cls._settings.mouse_btn = cls._settings.LEFT_CLICK
        cls._printer.custom_print(f'Изменил кнопку мыши на: {cls._settings.mouse_btn}')


def main():
    keyboard.add_hotkey(ClickerSettingsCollector.START_HOTKEY, lambda: Clicker.start_clicker())
    keyboard.add_hotkey(ClickerSettingsCollector.TOGGLE_MOUSE_HOTKEY, lambda: Clicker.toggle_mouse_btn())
    keyboard.wait()


if __name__ == '__main__':
    main()