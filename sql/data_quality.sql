-- DATA QUALITY AUDIT: OList Dataset
-- This script evaluates the dataset through checking for row counts, missing 
-- values, relationships between tables, and duplicate records.

-- Row Counts: Understand how much data exists in each table
with row_counts as (
	select 'orders' as table_name,
	count(*) as row_count
	from orders
union all
	select 'customers',
	count(*)
	from customers
union all
	select 'products',
	count(*)
	from products
)
select * from row_counts;

-- Null Value Analysis: Identify missing values in key columns
with order_nulls as (
	select
		count(*) as total_orders,
		count(customer_id) as non_null_customer_id,
		count(order_purchase_timestamp) as non_null_purchase_time
	from orders
),
product_nulls as (
	select
		count(*) as total_products,
		count(product_category_name) as non_null_category
	from products
)
select * from order_nulls, product_nulls;

-- Check Referential Integrity: Verify validity of table relationships
-- (if any of these values are greater than 0, there's a real data issue)
select count(*) as orphan_orders
from orders as o
left join customers as c
	on o.customer_id = c.customer_id
where c.customer_id is null;
select count(*)
from order_items as oi
left join orders as o
	on oi.order_id = o.order_id
where o.order_id is null;
select count(*)
from order_items as oi
left join products as p
        on oi.product_id = p.product_id
where p.product_id is null;
select count(*)
from order_items as oi
left join sellers as s
        on oi.seller_id = s.seller_id
where s.seller_id is null;

-- Duplcate Check: Make sure unique IDs are not duplicated
select order_id,
	count(*)
from orders
group by order_id
having count(*) > 1;
select customer_id,
        count(*)
from customers
group by customer_id
having count(*) > 1;
select order_id,
	product_id,
        count(*)
from order_items
group by order_id, product_id
having count(*) > 1;

-- Check Date Range & Logical Consistence: Ensure time data makes sense
select
	min(order_purchase_timestamp) as first_order,
	max(order_purchase_timestamp) as last_order
from orders;
-- Check if delivery occured before purchase (Logical error)
select *
from orders
where order_delivered_customer_date < order_purchase_timestamp;
-- Estimated delivery before purchase
select *
from orders
where order_estimated_delivery_date < order_purchase_timestamp;

-- Other Data Anomalies: check for "weird" data
-- Negative/Zero Prices
select *
from order_items
where price <= 0;
-- Negative Shipping Cost
select *
from order_items
where freight_value < 0;
-- Invalid Review Scores
select *
from order_reviews
where review_score not between 1 and 5;
-- Missing Categories
select count(*)
from products
where product_category_name is null;
