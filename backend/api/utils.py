import csv
import io

import xlsxwriter

from django.http import HttpResponse


def get_csv_or_xlsx(queryset, attr, type):
    """Получить файл csv или xlsx на основе запроса queryset, по заданным
        атрибутам"""
    values = list(queryset.values_list(*attr))
    file_name = f'{queryset.model._meta.model_name}.{type}'
    if type == 'excel':
        output = io.BytesIO()
        file = xlsxwriter.Workbook(output)

        worksheet = file.add_worksheet('List1')
        worksheet.write_row('A1', attr)

        for row in range(len(values)):
            worksheet.write_row(f'A{row+2}', values[row])

        file.close()
        output.seek(0)

        response = HttpResponse(output, content_type='application/ms-excel')
        response['Content-Disposition'] = (f'attachment; '
                                           f'filename = {file_name}')
        return response

    elif type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        writer = csv.writer(response)
        writer.writerow(attr)
        for value in values:
            writer.writerow(value)

        return response
    raise ValueError('Передан не правильный параметр, ожидалось csv или excel')