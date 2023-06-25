from preprocessing_pipeline.preprocessing_script import runner
from model_result.model_output import model_runner


def init_method(JobID):
    #TODO: Get JobID from prateek data collection service
    #change all relative directories if required
    runner(JobID)
    model_runner(JobID)
    
if __name__ == "__main__":
    init_method()

