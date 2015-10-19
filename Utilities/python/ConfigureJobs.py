import datetime
import UserInput

def getJobName(sample_name, selection):
    date = '{:%Y-%m-%d}'.format(datetime.date.today())
    return '-'.join([date, sample_name, selection])
def getListOfFiles(filelist):
        data_path = "/afs/cern.ch/user/k/kelong/work/AnalysisDatasetManager/FileInfo"
        for name in filelist:
            if "*" not in name:
                yield name
            else:
                file_info = UserInput.readJson("/".join([data_path, "%s.json" % "data" if "data" in name else "montecarlo"]))
                for file_name in file_info.keys():
                    if name.strip("*") in file_name:
                        yield file_name
def getInputFilesPath(sample_name, selection):
    data_path = "/afs/cern.ch/user/k/kelong/work/AnalysisDatasetManager/FileInfo"
    selection_map = { "preselection" : "fsa",
            "Zselection" : "preselection",
            "Wselection" : "Zselection"
    }
    if selection not in selection_map.keys():
        raise ValueError("Invalid selection '%s'. Selection must correspond"
               " to a {selection}.json file" % sample_name)
    input_files = UserInput.readJson("/".join([data_path, "wz_analysis", "%s.json" 
        % selection_map[selection]]))
    if sample_name not in input_files.keys():
        raise ValueError("Invalid input file %s. Input file must correspond"
               " to a definition in MetaData/input_files.json" % sample_name)
    return input_files[sample_name]['file_path'].rstrip("/*")
def getCutsJsonName(selection):
    definitions_json = UserInput.readJson("Cuts/definitions.json")
    if selection not in definitions_json.keys():
        raise ValueError("Cut name must correspond to a definition in " 
            "Cuts/definitions.json")
    return definitions_json[selection]
def getTriggerName(input_files_path):
    trigger_names = ["MuonEG", "DoubleMuon", "DoubleEG"]
    if "data" in input_files_path:
        for name in trigger_names:
            if name in input_files_path:
                return "-t " + name
    return ""
