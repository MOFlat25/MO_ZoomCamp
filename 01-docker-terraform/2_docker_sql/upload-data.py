#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd




# In[35]:


pd.__version__


# In[36]:


df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)


# In[37]:


df


# In[38]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[39]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))


# In[40]:


from sqlalchemy import create_engine


# In[41]:


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[75]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[76]:


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)


# In[77]:


df = next(df_iter)


# In[78]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[79]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[15]:


--%time df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[80]:


from time import time


# In[83]:


while True: 
    t_start = time()

    df = next(df_iter)
    
    df.VendorID = pd.to_numeric(df.VendorID, downcast="integer") 
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.passenger_count = pd.to_numeric(df.passenger_count, downcast="integer") 
    df.trip_distance = pd.to_numeric(df.trip_distance, downcast="float") 
    df.RatecodeID = pd.to_numeric(df.RatecodeID, downcast="integer") 
    df.store_and_fwd_flag = df['store_and_fwd_flag'].astype(str)
    df.PULocationID = pd.to_numeric(df.PULocationID, downcast="integer") 
    df.DOLocationID = pd.to_numeric(df.DOLocationID, downcast="integer") 
    df.payment_type = pd.to_numeric(df.payment_type, downcast="integer") 
    df.fare_amount = pd.to_numeric(df.fare_amount, downcast="float") 
    df.extra = pd.to_numeric(df.extra, downcast="float") 
    df.mta_tax = pd.to_numeric(df.mta_tax, downcast="float") 
    df.tip_amount = pd.to_numeric(df.tip_amount, downcast="float") 
    df.tolls_amount = pd.to_numeric(df.tolls_amount, downcast="float") 
    df.improvement_surcharge = pd.to_numeric(df.improvement_surcharge, downcast="float") 
    df.total_amount = pd.to_numeric(df.total_amount, downcast="float") 
    df.congestion_surcharge = pd.to_numeric(df.congestion_surcharge, downcast="float") 

    
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))


# In[35]:


get_ipython().system('wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv')


# In[36]:


df_zones = pd.read_csv('taxi+_zone_lookup.csv')


# In[38]:


df_zones.head()


# In[42]:


df_zones.to_sql(name='zones', con=engine, if_exists='replace')


# In[ ]:




