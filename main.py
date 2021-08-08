import psycopg2
import psycopg2.extras
from flask import Flask, render_template, jsonify
import time



def get_stat(connection):
    cmd = '''DO $$
    DECLARE
      _query text;
      _name text;
    BEGIN
      _name := 'prepared_query';
      _query := '
        SELECT  DATE(''1970-01-01''::date + (time_started * interval ''1 second'')) as start_date
            '||(SELECT ', '||string_agg(DISTINCT 
                        ' sum(case when service ='||quote_literal(service)||' then 1 else 0 end) AS '||quote_ident(service),',') 
                FROM jobs)||'
        FROM jobs
        GROUP BY start_date
        ';

        BEGIN
            EXECUTE 'DEALLOCATE '||_name;
        EXCEPTION
            WHEN invalid_sql_statement_name THEN
        END;

        EXECUTE 'PREPARE '||_name||' AS '||_query;
    END
    $$;

    EXECUTE prepared_query;'''
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        # coldata = cursor.fetchall()
        # colnames = [desc[0] for desc in cursor.description]
        return [desc[0] for desc in cursor.description], cursor.fetchall()



def chartify_data(colnames, coldata):
    def gen_color():
        from random import randint
        d = (0, 255) # diapazon
        return (randint(*d), randint(*d), randint(*d), 1)



    # reorganize columns
    organized_data = {}
    for colindex in range (len (colnames)):  # first one is data
        organized_data[colnames[colindex]] = [i[colindex] for i in coldata]
    # generate datasets
    datasets = []
    for key in organized_data:
        if key=='start_date':
            continue
        print(gen_color())
        datasets.append({
                        "label": key ,
                        "data": organized_data[key],
                        "borderColor": "rgba{}".format(gen_color()),
                        "backgroundColor": "rgba(255, 255, 255, 0.0)"
                    })

    data = {
        "labels": organized_data['start_date'] ,
        "datasets": datasets,
        "borderColor": "rgba(255, 99, 132, 1)",
        "backgroundColor": "rgba(255, 255, 255, 0.0)"
    }
    return data


# conn = psycopg2.connect (dbname='afanasy' , user='afadmin' ,
#                          password='AfPassword' , host='10.2.67.101')
#
# colnames, data = get_stat(conn)
# chartify_data(colnames, data)

app = Flask(__name__)
# print(get_stat(conn)['start_date'])


@app.route('/', methods = ['POST', 'GET'])
def index():
    metadata = {'server ip':'127.0.0.1'}
    return render_template('index.html', meta = metadata)


@app.route('/data')
def config():
    colnames , data = get_stat(conn)
    return jsonify(chartify_data (colnames , data))


@app.route('/stat')
def stat():
    return  render_template('stat.html')

if __name__=='__main__':
    conn = psycopg2.connect (dbname='afanasy' , user='afadmin' ,
                             password='AfPassword' , host='10.2.67.101')
    app.run()