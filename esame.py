class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        try:
            with open(self.name, 'r') as my_file:
                lines = my_file.readlines()
                lines = lines[1:]
                
                if not lines:
                    return []
            
        except FileNotFoundError:
            raise ExamException(f'Il file {self.name} non esiste')
        except Exception as e:
            raise ExamException(f'Errore in apertura del file: {e}')

        dati = []
        
        old_parts = None

        for line in lines:
            parts = line.split(',')

            if len(parts) < 2:
                continue

            if len(parts) > 2:
                parts = parts[:2]

            if not (len(parts[0]) == 7 and parts[0][:4].isdigit() and parts[0][4] == '-' and parts[0][5:].isdigit()):
                continue
            
            curr_year, curr_month = [int(part) for part in parts[0].split('-')]
                        
            if curr_month < 1 or curr_month > 12:
                continue
            
            if old_parts is not None:
                if parts[0] == old_parts[0]:
                    raise ExamException(f'Ci sono delle date duplicate: {old_parts[0]}, {parts[0]}')
                
                old_year, old_month = [int(part) for part in old_parts[0].split('-')]
                
                if old_year == curr_year and old_month > curr_month:
                    raise ExamException(f'I mesi delle date non sono in ordine: {old_parts[0]}, {parts[0]}')
                if old_year > curr_year:
                    raise ExamException(f'Gli anni delle date non sono in ordine: {old_parts[0]}, {parts[0]}')

            old_parts = parts

            date, passengers = parts
            
            date = date.strip() 
            
            try:
                passengers = int(passengers.strip())
            except:
                continue

            if passengers <= 0:
                continue
            
            dati.append([date, passengers])

            
        return dati

def find_min_max(time_series):
    if time_series == []:
        return {}

    data = {}
    years_list = []

    first_year = int(time_series[0][0].split('-')[0])
    last_year = int(time_series[-1][0].split('-')[0])

    for year in range(first_year, last_year + 1):
        year_list = []
        
        for item in time_series:
            item_year = int(item[0].split('-')[0])
            
            if item_year == year:
                year_list.append(item)
                
        years_list.append([year, year_list])

    for year in years_list:
        if len(year[1]) == 1:
            data[str(year[0])] = {}
            continue

        data[str(year[0])] = {"min": [], "max": []}
        min_pass = min([item[1] for item in year[1]])
        max_pass = max([item[1] for item in year[1]])
        
        for item in year[1]:
            if item[1] == min_pass:
                data[str(year[0])]['min'].append(item[0].split('-')[1])
                
            if item[1] == max_pass:
                data[str(year[0])]['max'].append(item[0].split('-')[1])

    return data
