drop database modern_agriculture;
create database modern_agriculture;
use modern_agriculture;

create table admin(
admin_id int auto_increment primary key,
admin_name varchar(255) not null,
password varchar(255) not null
);

create table locations(
location_id int auto_increment primary key,
location_name varchar(255) not null,
zipcode varchar(255) not null
);

create table machinery_types(
machinery_type_id int auto_increment primary key,
machinery_type varchar(255) not null
);

create table machinery_providers(
machinery_provider_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
phone varchar(255) not null,
password varchar(255) not null,
address varchar(255) not null,
location_id int,
foreign key (location_id) references locations (location_id)
);



create table machineries(
machinery_id int auto_increment primary key,
machinery_name varchar(255) not null,
picture varchar(255) not null,
price_per_hour varchar(255) not null,
description varchar(255) not null,
status varchar(255) not null,
machinery_type_id int,
machinery_provider_id int,
foreign key (machinery_type_id) references machinery_types (machinery_type_id),
foreign key (machinery_provider_id) references machinery_providers (machinery_provider_id)
);

create table farmers(
farmer_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
phone varchar(255) not null,
password varchar(255) not null,
address varchar(255) not null
);

create table bookings(
booking_id int auto_increment primary key,
date varchar(255) not null,
from_date_time varchar(255) not null,
to_date_time varchar(255) not null,
status varchar(255) not null,
total_price varchar(255),
extra_charges varchar(255),
farmer_id int,
machinery_id int,
foreign key (farmer_id) references farmers (farmer_id),
foreign key (machinery_id) references machineries (machinery_id)
);



create table payments(
payment_id int auto_increment primary key,
amount varchar(255) not null,
date varchar(255) not null,
status varchar(255) not null,
cvv varchar(255) not null,
expiry_date varchar(255) not null,
card_number varchar(255) not null,
card_holder_name varchar(255) not null,
card_type varchar(255) not null,
booking_id int,
foreign key (booking_id) references bookings (booking_id),
farmer_id int,
foreign key (farmer_id) references bookings (farmer_id)
);

