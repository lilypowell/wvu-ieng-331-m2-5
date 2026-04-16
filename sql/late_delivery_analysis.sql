-- Business Question #2: What percentage of orders are delivered later than
-- estimated?
-- This query will compare the actual customer delivery date to the estimated
-- delivery date for delivered orders(ignoring the time-of-day differences). It will classify each order as early,
-- on time, or late. Then the number and percentages of orders in each 
-- category will be calculated.

with delivery_status as (
	select
		order_id,
		date(order_delivered_customer_date) as delivered_date,
		date(order_estimated_delivery_date) as estimated_date,
		case
			when date(order_delivered_customer_date) > date(order_estimated_delivery_date) then 'Late'
			when date(order_delivered_customer_date) = date(order_estimated_delivery_date) then 'On Time'
			else 'Early'
		end as delivery_status
	from orders
	where order_delivered_customer_date is not null
	and order_estimated_delivery_date is not null
)

select
	delivery_status,
	count(*) as order_count,
	round(count(*) * 100.0 / sum(count(*)) over(), 2) as percentage_of_orders
from delivery_status
group by delivery_status
order by 
	case delivery_status
		when 'Early' then 1
		when 'On Time' then 2
		when 'Late' then 3
	end;
