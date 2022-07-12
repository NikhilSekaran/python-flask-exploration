import logging
from flask import Flask, render_template, send_file
import download_package as dp
from flask_executor import Executor


class PortalFlask(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name, instance_relative_config=True)


# create and configure the app
app = PortalFlask(__name__)
executor = Executor(app)


def init_db():
    app.logger.info('inside init_db')
    import time
    time.sleep(5)
    for i in range(1, 10):
        print(f'int value: {i}')
        time.sleep(i)
    app.logger.info('inside init_db sleep completed')
    return f'Initialize database completed'


@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/init')
def init_database():
    app.logger.info('inside init_database')
    app.logger.info(f'Status: {executor.futures._state("init")}')
    if not executor.futures.done('init'):
        future_status = executor.futures._state('init')
        app.logger.info(f"status of init: {future_status}")
        if future_status:
            app.logger.info(
                f'Function output '
                f'{executor.futures.done(init_db)}')
            return '''
                               <html>
                                   <head>
                                       <title> Database Status </title>
                                   </head>
                                   <body>
                                       <h1>Database Initialization still in
                                       progress: About to Blast</h1>
                                   </body>
                               </html> '''
    else:
        futures = executor.futures.pop('init')
        # CALL db_drop_all
        # Call db.create_all
        app.logger.info(futures.result())
    app.logger.info('Trigger Init Database')
    executor.submit_stored('init', init_db)
    message = 'Database Triggered for Initialization'
    return render_template('status_page.html', message=message)


@app.route('/application-download')
def application_download():
    return render_template('download.html')


@app.route('/ACP<codeplug>_V<rel_version>.zip')
def get_package(codeplug, rel_version):
    app.logger.info(f'cp_num: {codeplug}, ver: {rel_version}')
    zip_file_name = dp.create_download_package()

    response = send_file(zip_file_name.name)
    return response


if __name__ == '__main__':
    logging.basicConfig(
        filename='web_application.log',
        level=logging.DEBUG,
        format="%(threadName)-10s %(asctime)s %(levelname)-8s %(message)s"
    )

    app.run(debug=True, port=5000)
