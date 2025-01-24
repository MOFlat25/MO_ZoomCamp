# Week One Homework 2024

## Question 1: Knowing Docker Tags
### Which docker tag has the following text?: 
*-Automatically remove the container when it exits*

Answer: rm

Commands:
```
docker --help
docker build --help
docker run --help

```



## Question 2: Understanding Docker First Run
### What version of the package wheel?

Answer: 0.45.1

Commands:
```
docker run -it --entrypoint bash python:3.9
pip list

```



## Question 3: Count Records
### How many taxi trips were totally made on 18 September 2019?
    
Answer: 15,612 trips were started and completed on 18 September 2019.

SQL Code:
```
-- There are no null fields in the datetime fields and we use a 
-- where filter, so we can use count(*) instead of count(column_name)


select
	cast(lpep_pickup_datetime as date) as pick_up_time,
	cast(lpep_dropoff_datetime as date) as drop_off_time,
	count(*) as trip_count
from green_taxi_trips
where 
	cast(lpep_pickup_datetime as date) = '2019-09-18'
	and cast(lpep_dropoff_datetime as date) = '2019-09-18'
group by
	pick_up_time,
	drop_off_time;
	
```



## Question 4: Longest trip for each day
### Which pick-up day had the longest trip distance?

Answer: 21 September 2019 had the longest trip distance of 135.53 miles compared to the other 3 dates.

SQL Code:
```
select
	cast(lpep_pickup_datetime as date) as pick_up_time,
	cast(lpep_dropoff_datetime as date) as drop_off_time,
	max(trip_distance) as longest_trip_distance
from green_taxi_trips
where 
	cast(lpep_pickup_datetime as date) in ('2019-09-16','2019-09-18','2019-09-21','2019-09-26')
	and cast(lpep_dropoff_datetime as date) in ('2019-09-16','2019-09-18','2019-09-21','2019-09-26')
	and cast(lpep_pickup_datetime as date) = cast(lpep_dropoff_datetime as date)
group by
	pick_up_time,
	drop_off_time
order by 
	longest_trip_distance desc;
	
```



## Question 5: Three Biggest Pick-Up Boroughs
### Which were the 3 pick-up boroughs that had a sum of total_amount superior to 50,000?
*Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown*

Answer: Brooklyn (approx $96,333), Manhattan (approx $92,271), & Queens (approx $78,671). 

SQL Code:
```
select
	l."Borough" as borough,
	cast(g.lpep_pickup_datetime as date) as pick_up_date,
	sum(g.total_amount) as total_amount_sum
from green_taxi_trips as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
group by 
	borough,
	pick_up_date
having 
	cast(g.lpep_pickup_datetime as date) = '2019-09-18'
	and l."Borough" != 'Unknown'
	and l."Borough" is not null
	and sum(g.total_amount) > 50000
order by
	total_amount_sum desc;

```


## Question 6: Largest Tip 
### For the passengers picked up in September 2019 in the zone name Astoria, which was the drop-off zone that had the largest tip? 
*We want the name of the zone, not the id.*

Answer: Woodside (data must have been updated). The largest tip in September 2019 
    from pick-up zone Astoria was $30 going to drop-off zone Woodside.

SQL Code:
```
--Version 1:
with Astoria as (
	select
		g."PULocationID" as pick_up_location_id,
		l."Zone" as pick_up_zone,
		g.tip_amount,
		g."DOLocationID" as drop_off_location_id
from green_taxi_trips as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
where 
	to_char(lpep_pickup_datetime, 'YYYY-MM') = '2019-09'
	and lower(l."Zone") = 'astoria'
)

select
	a.pick_up_location_id,
	a.pick_up_zone,
	l."Zone" as drop_off_zone,
	max(a.tip_amount)
from astoria as a
inner join taxi_lookup l
	on a.drop_off_location_id = l."LocationID"
group by 
	pick_up_location_id,
	pick_up_zone,
	drop_off_zone
order by
	max(a.tip_amount) desc;

--Version 2:
with Astoria as (
	select
		g."PULocationID" as pick_up_location_id,
		l."Zone" as pick_up_zone,
		g.tip_amount,
		g."DOLocationID" as drop_off_location_id
from green_taxi_trips as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
where 
	to_char(lpep_pickup_datetime, 'YYYY-MM') = '2019-09'
	and lower(l."Zone") = 'astoria'
)

select
	l."Zone" as drop_off_zone
from Astoria as a
inner join taxi_lookup l
	on a.drop_off_location_id = l."LocationID"
where 
	tip_amount = (select max(tip_amount)
		from Astoria 
		);
```



## Question 7: Creating Resources
### After updating the main.tf and variable.tf files run: 
```
terraform apply

```

Output:
```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "linen-fort-427318-d1"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning (known after apply)

      + website (known after apply)
    }
```