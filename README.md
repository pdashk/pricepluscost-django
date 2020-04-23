# PRICEPLUSCOST

Python Django-based project

## EIA Download

`eia` app collects and stores retail electricity price data from eia.gov

## CCMS Download

`ccms` app collects and stores appliance model energy efficiency attributes from U.S. Department of Energy

## Bestbuy Download

`bb` app collects product information from Bestbuy API.

## Maps

`maps` app matches products from one download sourcees to reference models from reference sources.

Admin panel gives option to add `Sources` and label them as either "Product Source" or "Reference Source". This differentiation will ultimately be used to create "Product Models" and "Reference Models".

Next, `Categories` are created for each source (each source must have a field that denotes something like a product category). From admin panel, can map `Categories` in many-to-many, symmetrical relationships; many because we want a mapping for each reference source. The mapping ultimately limits which models from each source will be matched.

> For example "Refrigerators" from the product source "Best Buy" can map to "Refrigerators and Freezers" from the reference source "CCMS" and "Refrigeration Equipment" from the reference source "ENERGY STAR". The reverse relationships will automatically be generated, but "Refrigerators and Freezers" from "CCMS" will not automatically be matched to "Refrigeration Equipment" from "ENERGY STAR". This match can be made, but a reference Category matching to another reference category has no purpose in this app. 

Next, `Manufacturers` are created from all sources. They are agnostic of source (including source type) and category. That is, `Manufacturers` having the same name will be the same entity across all sources and categories. `Manufacturers` are mapped to other `Manufacturers` in a many-to-many relationship in order to map categories. This mapping generates a field for whether the `Manufacturer` is "primary", meaning that other `Manufacturers` map to it. If a `Manufacturer` has at least one `Manufacturer` mapped to it (including itself), then it is considered "primary". If the `Manufacturer` maps to a primary, then it should have no other `Manufacturer` mapped to it (others should map to the same "primary")

> For example, if there are only unique `Manufacturers`, then each `Manufacturer` will map only to itself, and they will all be "primary".

Next, `Product Models` and `Reference Models` are created from their respective categories. `Product Models` are defined as having a "model number" and coming from a specific "primary manufacturer"; they are agnostic to source or category, except they must come from a category of a product source. `Reference Models` are the same, except they have "model number patterns" instead of "model numbers" and they must come from a category of a reference source.

## PPC Items

`ppc` app integrates downloaded data into items for viewing.