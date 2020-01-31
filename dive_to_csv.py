import csv
import os
from datetime import timedelta
import fitparse

# the header fields appearing in the output csv file.  These fields are renamed versions of what appears in the
# fit field list.
header_fields = ['timestamp', 'type', 'accel_x', 'accel_y', 'accel_z', 'heart_rate', 'lat', 'lon']


def convert_dir_fit_to_csv(input_dir, output_dir):
    """
    converts directory of .fit files to a directory of .csv flues
    :param input_dir: input directory containing .fit files
    :param output_dir: output directory where .csv files go
    """
    files = os.listdir(input_dir)
    fit_files = [file for file in files if file[-4:].lower() == '.fit']

    for file in fit_files:
        in_file = os.path.join(input_dir, file)
        out_file = os.path.join(output_dir, file[:-4] + '.csv')

        print(f'converting {in_file}')
        convert_fit_to_csv(in_file, out_file)
    print('finished conversions')


def convert_fit_to_csv(in_file, out_file):
    """
    convert .fit file to .csv file.  Note, only certain fields are processed based on the dive project.
    :param in_file: input fit file
    :param out_file: output csv file
    """
    fit_parse = fitparse.FitFile(in_file, data_processor=fitparse.StandardUnitsDataProcessor())

    data = []
    for m in fit_parse.messages:
        if not hasattr(m, 'fields'):
            continue

        # for debug - print out all the fields in the message - can use this to look at the all available information
        # print(m.fields)

        # turn m.fields array into a fields dictionary for ease of processing (lookup by name)
        fields = {k.name: k.value for k in m.fields}
        if 'compressed_calibrated_accel_x' in fields:
            timestamp = fields['timestamp']
            num_samples = len(fields['compressed_calibrated_accel_x'])
            for i in range(num_samples):
                # turn this row into the multiple rows dimensioned by number of samples.  The timestamp is adjusted
                # to offset by the number of samples taken within the message
                row = {'type': 'A',
                       'timestamp': timestamp + timedelta(milliseconds=(i * 1000 / num_samples)),
                       'accel_x': fields['compressed_calibrated_accel_x'][i],
                       'accel_y': fields['compressed_calibrated_accel_y'][i],
                       'accel_z': fields['compressed_calibrated_accel_z'][i],
                       }
                data.append(row)
        elif 'heart_rate' in fields:
            row = {'type': 'H',
                   'timestamp': fields['timestamp'],
                   'heart_rate': fields['heart_rate']}
            data.append(row)
        elif 'position_lat' in fields:
            row = {'type': 'G',
                   'timestamp': fields['timestamp'],
                   'lat': fields['position_lat'],
                   'lon': fields['position_long']}
            data.append(row)

    # write out csv
    with open(out_file, 'w') as f:
        writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=header_fields)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    convert_dir_fit_to_csv('input', 'output')