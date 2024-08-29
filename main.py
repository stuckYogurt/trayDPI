import rumps
import subprocess
from webbrowser import open as webopen

params = {
    #   exec core
    'addr': '127.0.0.1',
    'debug': False,
    'dns-addr': '8.8.8.8',
    'dns-port': '53',
    # dpi over https
    'doh': False,
    # bypass DPI only on packets matching this regex pattern
    'regex': '',
    'port': '8080',
    'timeout': '2000',
    #bypass only on this url
    'url': '',
    'window-size': '50',

    #   access
    'default-path-params': '~/Library/Caches/',
    'default-path-exec': '~/.spoof-dpi/bin/spoof-dpi',

    'show-terminal-output ': True,
}

cmd = ''

class StatusBarApp( rumps.App ):
    def __init__(self):
        super(StatusBarApp, self).__init__('trayDPI', menu=self.areaSet())


        # print(self.properties)
        # print(self.properties.values())
        # print(self.properties.items())

    def areaSet(self):
        self.turnButt = rumps.MenuItem(title='Turn on')
        self.properties = rumps.MenuItem(title='Properties')
        for e in params:
            self.properties[e] = rumps.MenuItem(
                title = '{}: {}'.format(e, params[e]),
                key = e,
                callback = self.foo
            )
            print(self.properties[e])

        return [self.turnButt, self.properties, 'About']


    @rumps.clicked('Turn on')
    def button(self, sender):
        if sender.title == 'Turn on':

            self.termProcess = subprocess.Popen(self.getCMD(), stdout=subprocess.PIPE, shell=True, universal_newlines=True)
            # if self.termProcess.returncode != 0:
            #     rumps.Window(
            #         message="Something went wrong during script hangling", title='error',
            #         default_text="Process finished with returncode: {}".format(self.termProcess.returncode)
            #     )
            sender.title = 'Turn off'
        else:
            sender.title = 'Turn on'
            commCallback = self.termProcess.stdout.read()
            self.termProcess.terminate()
            self.termProcess.wait()
            print("Process finished with returncode: {}".format(self.termProcess.returncode))
            print(commCallback)

            if params['show-terminal-output']:
                newWind = rumps.Window(
                    message="Process finished with returncode: {}".format(self.termProcess.returncode),
                    title="Returncode",
                    default_text = commCallback
                )

                newWind.run()

    @rumps.clicked('About')
    def about(self, _):
        webopen('https://github.com/stuckYogurt/trayDPI')

    # callback for properties buttons
    def foo(self,sender):
        if type(params[sender.key]) is bool:
            params[sender.key] = not params[sender.key]
        else:
            wind = rumps.Window(
                message = "Insert new value for {}".format(sender.key),
                title = "Value change",
                default_text = params[sender.key],
                cancel = True
            )

            resp = wind.run()
            if resp.clicked:
                params[sender.key] = resp.text
            else: print('canceled')

        self.properties[sender.key].title = "{}: {}".format(sender.key, params[sender.key])

        print(params[sender.key])

        self.restart()

    def getCMD(self):
        return params['default-path-exec'] + ' -addr ' + params['addr'] + \
                (' -debug ' if params['debug'] else ' ') + \
                '-dns-addr ' + params['dns-addr'] + \
                ' -dns-port ' + params['dns-port'] + \
                (' -enable-doh ' if params['doh'] else ' ') + \
                (('-pattern '+params['regex']) if params['regex'] else '') + \
                '-port ' + params['port'] + \
                ' -timeout ' + params['timeout'] + \
                ((' -url ' + params['url']) if params['url'] else '') + \
                ' -window-size ' + params['window-size'] + ' -no-banner'

    def restart(self):
        if self.turnButt.title == 'Turn off':
            self.termProcess.terminate()
            self.termProcess.wait()
            print("Process finished with returncode: {}".format(self.termProcess.returncode))



            self.termProcess = subprocess.Popen(self.getCMD().split(), shell=params['open-shell'])

StatusBarApp().run()