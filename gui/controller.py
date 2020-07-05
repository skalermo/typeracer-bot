class Controller:
    def __init__(self, app, bot, ui):
        self.app = app
        self.bot = bot
        self.ui = ui

    def start_race(self):
        print('Starting race...')
        print(f'Estimated time of completion: {self.bot.expected_time_s} s')
        self.bot.start_race()
        print('Race finished.')

    def get_text(self):
        print('Getting text...')
        self.bot.get_text()
        self.ui.textEdit.setText(self.bot.text_to_type)

    def speed_changed_slider(self):
        new_speed = self.ui.speedSlider.value()
        self.ui.speedLine.setText(str(new_speed))
        self.bot.update_speed(new_speed)
        print(f'Changed typing speed to {new_speed}')

    def speed_changed_editText(self):
        new_speed = int(self.ui.speedLine.text())
        self.ui.speedSlider.setValue(new_speed)
        self.bot.update_speed(new_speed)
        print(f'Changed typing speed to {new_speed}')

    def close_all(self):
        print('Exiting...')
        self.app.quit()


