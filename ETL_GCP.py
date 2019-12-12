# https://cloud.google.com/python/setup
# pip install --upgrade google-cloud-bigquery
import os
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)


class GCP:
	def print_hello(self):
		print('yo whatsup')

	def __init__(self):
		self.client = self.initialize_connection_to_GCP()
		self.project_id = 'calotrack-1050-final'
		self.dataset_id = 'nutrition'
		self.branded_table_id = 'branded_table'
		self.common_table_id = 'common_table'
		self.exercise_table_id = 'exercise_table'
		self.bucket = 'calotrack-data'
		
	def initialize_connection_to_GCP(self):
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser('~/.credentials/MyGCPCredentials.json')
		return bigquery.Client()

	def update_branded_table(self, add_branded_table):
		logging.debug("UPDATING BRANDED TABLE...")
		add_branded_table.to_csv("update_data/branded_to_add.csv", index=False)
		new_table_loc = "update_data/branded_to_add.csv"
		self.upload_file(self.bucket, new_table_loc, "branded_to_add.csv")

		"""
		https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#appending_to_or_overwriting_a_table_with_csv_data
		"""
		table_ref = self.client.dataset(self.dataset_id).table(self.branded_table_id)
		job_config = bigquery.LoadJobConfig()
		# can change this to WRITE_EMPTY that writes only if table is empty
		# or to WRITE_TRUNCATE which truncates the table before writing
		job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
		# The source format defaults to CSV, so the line below is optional.
		job_config.source_format = bigquery.SourceFormat.CSV
		# get the URI by https://cloud.google.com/bigquery/docs/loading-data-cloud-storage#gcs-uri
		uri = "gs://calotrack-data/branded_to_add.csv"
		load_job = self.client.load_table_from_uri(
		    uri, table_ref, job_config=job_config
		)  # API request
		logging.debug("Starting job {}".format(load_job.job_id))

		load_job.result()  # Waits for table load to complete.
		logging.debug("Job finished.")

		destination_table = self.client.get_table(table_ref)
		logging.debug("Loaded {} rows.".format(destination_table.num_rows))

	def update_common_table(self, add_common_table):
		logging.debug("UPDATING COMMON TABLE...")
		add_common_table.to_csv("update_data/common_to_add.csv", index=False)
		new_table_loc = "update_data/common_to_add.csv"
		self.upload_file(self.bucket, new_table_loc, "common_to_add.csv")

		"""
		https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#appending_to_or_overwriting_a_table_with_csv_data
		"""
		table_ref = self.client.dataset(self.dataset_id).table(self.common_table_id)
		job_config = bigquery.LoadJobConfig()
		# can change this to WRITE_EMPTY that writes only if table is empty
		# or to WRITE_TRUNCATE which truncates the table before writing
		job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
		# The source format defaults to CSV, so the line below is optional.
		job_config.source_format = bigquery.SourceFormat.CSV
		# get the URI by https://cloud.google.com/bigquery/docs/loading-data-cloud-storage#gcs-uri
		uri = "gs://calotrack-data/common_to_add.csv"
		load_job = self.client.load_table_from_uri(
		    uri, table_ref, job_config=job_config
		)  # API request
		logging.debug("Starting job {}".format(load_job.job_id))

		load_job.result()  # Waits for table load to complete.
		logging.debug("Job finished.")

		destination_table = self.client.get_table(table_ref)
		logging.debug("Loaded {} rows.".format(destination_table.num_rows))

	def update_exercise_table(self, add_exercise_table):
		logging.debug("UPDATING EXERCISE TABLE...")
		add_exercise_table.to_csv("update_data/exercise_to_add.csv", index=False)
		new_table_loc = "update_data/exercise_to_add.csv"
		self.upload_file(self.bucket, new_table_loc, "exercise_to_add.csv")

		"""
		https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#appending_to_or_overwriting_a_table_with_csv_data
		"""
		table_ref = self.client.dataset(self.dataset_id).table(self.exercise_table_id)
		job_config = bigquery.LoadJobConfig()
		# can change this to WRITE_EMPTY that writes only if table is empty
		# or to WRITE_TRUNCATE which truncates the table before writing
		job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
		# The source format defaults to CSV, so the line below is optional.
		job_config.source_format = bigquery.SourceFormat.CSV
		# get the URI by https://cloud.google.com/bigquery/docs/loading-data-cloud-storage#gcs-uri
		uri = "gs://calotrack-data/exercise_to_add.csv"
		load_job = self.client.load_table_from_uri(
		    uri, table_ref, job_config=job_config
		)  # API request
		logging.debug("Starting job {}".format(load_job.job_id))

		load_job.result()  # Waits for table load to complete.
		logging.debug("Job finished.")

		destination_table = self.client.get_table(table_ref)
		logging.debug("Loaded {} rows.".format(destination_table.num_rows))

	def upload_file(self, bucket_name, source_file_name, destination_blob_name):
	    """
	    Uploads a file to the bucket.
	    https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
	    """
	    storage_client = storage.Client()
	    bucket = storage_client.get_bucket(bucket_name)
	    blob = bucket.blob(destination_blob_name)

	    blob.upload_from_filename(source_file_name)

	    logging.debug('File {} uploaded to {}.'.format(
	        source_file_name,
	        destination_blob_name))

