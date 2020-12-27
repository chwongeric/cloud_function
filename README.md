# Simple proof of concept - spray and aggregation in ElasticSearch via GCP CloudFunction



## Architecture
![alt text](https://github.com/chwongeric/cloud_function/blob/main/images/es_cloud_func.png?raw=true)

## Raw Data: json array
> [{“key” : “9f7bba2f-51df-48fc-9da4-9bf5da67b152”,“name” : “AC Compressor Gasket”,“quantity” : 7153},
> ...
> ]


## DataSink: elasticsearch
> `{“key” : “9f7bba2f-51df-48fc-9da4-9bf5da67b152",“name” : “AC Compressor Gasket”,“quantity” : 512345,“first_received” : “2019-07-09”, “number_of_days_received” : 38, “last_received” : “2020-09-17"}`

## GCP Setup:
* VPC (firewall):  
	* add new ingress rule (elasticsearch) allow tcp:9200
* API:  enable logging, build (for Cloud Function)
* Pubsub:  
	1. 	From GCP management console:  create topic (give it name: inventory) 
	2. note down topic name for future debug use - should be like:  projects/{project-id}/topics/inventory
* Elasticsearch:   
	* Debian VM image, run following:
		1. `$ git clone https://github.com/chwongeric/cloud_function.git`
		2. Install by running: cloud_function/PubSub-Function-ES/setup/elastic_debian.sh
		3. `$ sudo vi /etc/elasticsearch/elasticsearch.yml  `(modify following 2 lines):
			* network.host: 0.0.0.0
			* cluster.initial_master_nodes: ["node-1"]
		4. `$ sudo systemctl start elasticsearch.service`
		5. `$ curl http://{VM public IP}:9200  (check services up and running via public IP)`
		6. other manual install detail see:  [https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)

	* 	Managed elastic service:  marketplace product depends on vendor discount and approval from Elastic, detail see:  [https://www.elastic.co/partners/google-cloud](https://www.elastic.co/partners/google-cloud)

* Cloud Function:  
	1. Trigger:  Topic: inventory, Mem allocated (256MB)
	2. Runtime: Python3.8, Ingress settings: allow all traffic
	3. Runtime environment variable - convenient for passing setup specific info like Elasticsearch service endpoint for example:
		* 	ELASTICSEARCH_IP={your VM public IP}
	4. Code: 
		1. `	$ git clone https://github.com/chwongeric/cloud_function.git`
		2. From GCP management console, inside Cloud Functions, select Edit-> Source, copy code from following 2 from PubSub-Function-ES/src to here:
			* 	main.py
			*  requirements.txt
	
		[Note]: this code will use runtime environment variable for flexibility of config like Elasticsearch service IP and Customer name (if not 'acme')
	
* Testing (from gcloud shell for simplicity):  used for generating test data (if no real data) and trigger sprayer and verify in Elastic
	1. 	`$ gcloud config set project {project-id}`
	2. 	`$ python3 -m pip install google.cloud`
	3. 	`$ git clone https://github.com/chwongeric/cloud_function.git`
	4. 	`$ cd PubSub-Function-ES/test`
	5. Depends on if there is already raw data or need to generate, the following will slice json raw data and push into pubsub message for cloud function to process in chunks:
		* 	If already has data - after copy data from cloud storage to here as INVENTORY.json, run following:
		
		`	$ ./cloudshell_test.sh {your project ID}`
			
		* 	If need to generate test raw data and test - run following:
		
		`	$ ./cloudshell_test.sh {your project ID} 100000`
			
			(this above will generate 100k sample json records and push into pubsub
			
	6. In management console can watch logs for cloud function processing status and metrics
	7. Verify data in Elasticsearch use following command as example:

`		$ ./es_test.py -i {Elasticsearch public IP} -p 9200 -n True`
		
  To cross check with a record can do following as example to query a specific key (UUID) against record in INVENTORY.json after running few days:
		
`		$ head -c 400 INVENTORY.json`
		
> [{"key": "f425b57b-c9ee-4a86-b2fe-886699b9590b", "name": "item 0", "quantity": 0}, {"key": "b22e7150-446c-4976-8fa1-f5a705fa39f3", "name": "item 1", "quantity": 1}, {"key": "ec5de262-59df-4942-93a0-3f9dc3463657", "nam
> e": "item 2", "quantity": 2}, {"key": "dccba960-7c8a-4be9-aa17-e8f674007b63".....

       $ ./es_test.py -i {Elasticsearch public IP} -p 9200 -k dccba960-7c8a-4be9-aa17-e8f674007b63
       
> {'key': 'dccba960-7c8a-4be9-aa17-e8f674007b63', 'name': 'item 3', 'quantity': 6, 'first_received': '2020-12-25', 'last_received': '2020-12-26', 'number_of_days_received': 2}


## More detail test result and cost analysis see pdf inside this repo
			

		


	
