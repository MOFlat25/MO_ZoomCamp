# Week One Homework 2025


## Question 1: Understanding Docker First Run
### Run docker with the ```puthon:3.12.8``` image in an interactive mode, use the entrypoint ```bash```.
### What's the version of ```pip``` in the image?

Answer: 24.3.1

Commands:
```
docker run -it --entrypoint bash python:3.12.8
pip --version

```

## Question 2: Understanding Docker Networking and docker-compose
### Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect ### to the postgres database?

Answer: db:5432

```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

```


## Question 3: Trip Segmentation Count
### During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, ###respectively, happened:

#### 1. Up to 1 mile
#### 2. In between 1 (exclusive) and 3 miles (inclusive),
#### 3. In between 3 (exclusive) and 7 miles (inclusive),
#### 4. In between 7 (exclusive) and 10 miles (inclusive),
#### 5. Over 10 miles

Answer:
    1. Up to 1 mile: 78,964
    2. In between 1 (exclusive) & 3 miles (inclusive): 150,850
    3. In between 3 (exclusive) & 7 miles (inclusive): 90,020
    4. In between 7 (exclusive) & 10 miles (inclusive): 24,074
    5. Over 10 miles: 32,294

SQL Code

```
--Version 1
select
	case
		when trip_distance <= 1.00 then 'Up to 1 Mile'
		when trip_distance > 1.00 and trip_distance <= 3.00 then '1-3 Miles'
		when trip_distance > 3.00 and trip_distance <= 7.00 then '3-7 Miles'
	 	when trip_distance > 7.00 and trip_distance <= 10.00 then '7-10 Miles'
		when trip_distance > 10.00 then '10+ Miles'
		else 'Error'
	end as trip_distance_grouped,
	count(*) as trip_count
from green_taxi_trips_oct19
where 
  lpep_pickup_datetime >= '2019-10-01 00:00:00' 
  and lpep_pickup_datetime < '2019-11-01 00:00:00'
  and lpep_dropoff_datetime >= '2019-10-01 00:00:00'
  and lpep_dropoff_datetime < '2019-11-01 00:00:00'
  and trip_distance is not null
  and lpep_pickup_datetime is not null
  and lpep_dropoff_datetime is not null
group by trip_distance_grouped
order by trip_distance_grouped;


--Version 2
select
	sum(case when trip_distance <= 1.00 then 1 else 0 end) as "Up to 1 Miles",
	sum(case when trip_distance > 1.00 and trip_distance <= 3.00 then 1 else 0 end) as "1-3 Miles",
	sum(case when trip_distance > 3.00 and trip_distance <= 7.00 then 1 else 0 end) as "3-7 Miles",
	sum(case when trip_distance > 7.00 and trip_distance <= 10.00 then 1 else 0 end) as "7-10 Miles",
	sum(case when trip_distance > 10.00 then 1 else 0 end) "10+ Miles"
from green_taxi_trips_oct19
where 
  lpep_pickup_datetime >= '2019-10-01 00:00:00' 
  and lpep_pickup_datetime < '2019-11-01 00:00:00'
  and lpep_dropoff_datetime >= '2019-10-01 00:00:00'
  and lpep_dropoff_datetime < '2019-11-01 00:00:00'
  and trip_distance is not null
  and lpep_pickup_datetime is not null
  and lpep_dropoff_datetime is not null;

```
## Question 4: Longest Trip for Each Day
### Which was the pick-up day with the longest trip distance? Use the pick-up time for your calculations.
*Tip: For every day, we only care about one single trip with the longest distance.*

Answer: 11 October 2019 was the day with the longest trip distance out of the 4 dates, with a trip distance of 95.78 miles.

SQL Code:
```
select
	cast(lpep_pickup_datetime as date) as pick_up_time,
	cast(lpep_dropoff_datetime as date) as drop_off_time,
	max(trip_distance) as longest_trip_distance
from green_taxi_trips_oct19
where 
	cast(lpep_pickup_datetime as date) in ('2019-10-11','2019-10-24','2019-10-26','2019-10-31')
	and cast(lpep_dropoff_datetime as date) in ('2019-10-11','2019-10-24','2019-10-26','2019-10-31')
	and cast(lpep_pickup_datetime as date) = cast(lpep_dropoff_datetime as date)
group by
	pick_up_time,
	drop_off_time
order by 
	longest_trip_distance desc;

```

## Question 5: Three Biggest Pick-Up Zones
### Which were the top pick-up locations with over 13,000 in ```total_amount``` (across all trips) for 2019-10-18? 
*Consider only ```lpep_pickup_datetime``` when filtering by date.*

Answer: The top 3 pick-up locations with over $13,000 in ```total_amount``` were East Harlem North (approx $18,686.68), East Harlem South (approx $16,797.26), and Morningside Heights (approx $13,029.79).

SQL Code:
```
select
	l."Zone" as PUZone,
	cast(g.lpep_pickup_datetime as date) as pick_up_date,
	sum(g.total_amount) as total_amount_sum
from green_taxi_trips_oct19 as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
group by 
	PUZone,
	pick_up_date
having 
	cast(g.lpep_pickup_datetime as date) = '2019-10-18'
	and l."Zone" != 'Unknown'
	and l."Zone" is not null
	and sum(g.total_amount) > 13000
order by
	total_amount_sum desc;

```

## Question 6: Largest Tip
### For the passenger picked up in October 2019 in the zone named "East Harlem North," which was the drop-off zone that had the largest tip? 
*We need the zone, not the ID.*

Answer: JFK Airport. The tip was $87.30.

SQL Code:
```
--Version 1:
with East_Harlem_N as (
	select
		g."PULocationID" as pick_up_location_id,
		l."Zone" as pick_up_zone,
		g.tip_amount,
		g."DOLocationID" as drop_off_location_id
from green_taxi_trips_oct19 as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
where 
	to_char(lpep_pickup_datetime, 'YYYY-MM') = '2019-10'
	and lower(l."Zone") = 'east harlem north'
)

select
	h.pick_up_location_id,
	h.pick_up_zone,
	l."Zone" as drop_off_zone,
	max(h.tip_amount)
from East_Harlem_N as h
inner join taxi_lookup l
	on h.drop_off_location_id = l."LocationID"
group by 
	pick_up_location_id,
	pick_up_zone,
	drop_off_zone
order by
	max(h.tip_amount) desc;

--Version 2:
with East_Harlem_N as (
	select
		g."PULocationID" as pick_up_location_id,
		l."Zone" as pick_up_zone,
		g.tip_amount,
		g."DOLocationID" as drop_off_location_id
from green_taxi_trips_oct19 as g
inner join taxi_lookup as l
	on g."PULocationID" = l."LocationID"
where 
	to_char(lpep_pickup_datetime, 'YYYY-MM') = '2019-10'
	and lower(l."Zone") = 'east harlem north'
)

select
	l."Zone" as drop_off_zone
from East_Harlem_N as g
inner join taxi_lookup l
	on g.drop_off_location_id = l."LocationID"
where 
	tip_amount = (select max(tip_amount)
		from East_Harlem_N 
		);

```

## Question 7: Terraform Workflow
### Which of the following sequences, respectively, describe the workflow for:
####    1. Downloading the provider plugins and setting up backend.
####    2. Generating proposed changes and auto-executing the plan.
####    3. Remove all resources managed by terraform.

Answer:
```
    1. terraform init
    2. terraform apply -auto apply
    3. terraform destroy
```
