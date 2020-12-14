"""
Reads a configuration file containing settings for the package
"""
import configparser

class Config():
    """ Exposes all settings listed in a valid configuration file (*.ini) as
        object attributes. Use as Config.setting, i.e. Config.Quality """

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def __getattr__(self, key):
        setting_value = [self.config[section].get(key)
                         for section in self.config.sections()
                         if self.config[section].get(key)]

        return self._parse_setting_value(setting_value)

    def _parse_setting_value(self, setting_value):
        if self._is_boolean(setting_value):
            return True
        return self._converted_value(setting_value)

    def __str__(self):
        print(self.__dict__)
        options = ["Settings loaded from '{}':".format(self.config_file)]
        for section in self.config.sections():
            options.append("\tSection: {}".format(section))
            for option in self.config.options(section):
                options.append("\t\t{}: {}".format(option, self.config.get(section, option)))
        return '\n'.join(options)

    @staticmethod
    def _is_boolean(setting_value):
        if setting_value == "True":
            return True
        return False

    @staticmethod
    def _converted_value(setting_value):
        try:
            setting_value = float(setting_value[0])
        except ValueError:
            return setting_value[0]
        except IndexError:
            return setting_value
        return setting_value
