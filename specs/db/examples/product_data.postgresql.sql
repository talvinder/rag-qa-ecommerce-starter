-- POSTGRESQL Migration for product_data
-- Generated from database specification

CREATE TABLE product_data (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL
);


-- Add comments
COMMENT ON TABLE product_data IS 'Product data schema for e-commerce items including specifications like price, processor, RAM, camera, etc.';
COMMENT ON COLUMN product_data.id IS 'Primary key identifier';
COMMENT ON COLUMN product_data.name IS 'Product name';
COMMENT ON COLUMN product_data.price IS 'Product price';
