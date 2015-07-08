#!/usr/bin/python
#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Functions and classes for working with EMOD output files
"""
import json
import os
import csv
from zipfile import ZipFile
from vecnet.emod.output.binnedreport import BinnedReport
import zipfile

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "..", "tests", "output", "1")

def convert_to_csv(output_dir):
    filename = os.path.join(output_dir, "InsetChart.json")
    output_filename = "output.csv"
    inset_chart = json.load(open(filename))
    try:
        with open(os.path.join(output_dir, "DemographicsSummary.json")) as fp:
            demographics_summary = json.load(fp)
    except IOError:
        # No DemographicsSummary.json
        demographics_summary = None

    table = []
    field_names = ["Timestep"]

    timesteps = inset_chart["Header"]["Timesteps"]
    for i in range(0, timesteps):
        table.append({"Timestep": i})

    # Add data from InsetCharts.json
    for channel in inset_chart["Channels"]:
        data = inset_chart["Channels"][channel]["Data"]
        for i in range(0, len(data)):
            table[i][channel] = data[i]
        field_names.append(channel)

    # Add data from DemographicsSummary.json
    if demographics_summary is not None:
        for channel in demographics_summary["Channels"]:
            data = demographics_summary["Channels"][channel]["Data"]
            for i in range(0, len(data)):
                table[i][channel] = data[i]
            field_names.append(channel)

    # Add data from VectorSpeciesReport.json
    try:
        vector_species_report = BinnedReport(os.path.join(output_dir, "VectorSpeciesReport.json"))
        for channel in vector_species_report.channels:
            for species in vector_species_report.get_meanings_per_axis("Vector Species"):
                    data = vector_species_report.get_data(channel, "Vector Species", species)
                    for i in range(0, len(data)):
                        table[i][channel + ": " + species] = data[i]
                    field_names.append(channel + ": " + species)
    except IOError:
        # No VectorSpeciesReport.json, move on
        pass

    # Add data from BinnedReport.json
    try:
        binned_report = BinnedReport(os.path.join(output_dir, "BinnedReport.json"))
        for channel in binned_report.channels:
            for species in binned_report.get_meanings_per_axis("Age"):
                    data = binned_report.get_data(channel, "Age", species)
                    for i in range(0, len(data)):
                        table[i][channel + ": " + species] = data[i]
                    field_names.append(channel + ": " + species)
    except IOError:
        # No BinnedReport.json, move on
        pass

    # Write CSV file
    with open(os.path.join(output_dir, output_filename), "wb") as fp:
        writer = csv.DictWriter(fp, fieldnames=field_names)
        writer.writeheader()
        for row in table:
            writer.writerow(row)

    # Zip and compress CSV file
    with ZipFile(os.path.join(output_dir, "%s.zip" % output_filename), 'w') as myzip:
        myzip.write(os.path.join(output_dir, output_filename), output_filename, zipfile.ZIP_DEFLATED)
    return table

if __name__ == "__main__":
    convert_to_csv(base_dir)