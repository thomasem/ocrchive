Name ideas:
1. Wrinkle
2. Crumple
3. Tear
4. Faded
5. Tick
6. Steep
7. 


Base Features:
1. Scans in receipts (tries to deal with even worn, crumpled, disfigured receipts) and extracts text to understand what what was purchased, how much, and for how much
2. Two main types of receipts: those meant to simply be parsed and archived (such as for warranty, returns, etc.) and those that get included in expense tracking and categorization
3. Applies categories to each line-item, and keeps track of which store it was purchased from; categories are the default way to slice the data, but should support doing so by category (sub categories included? Such as Produce -> Green -> Kale, Lettuce, Broccoli?), which store, ...?
4. Users on each account can configure individual units of a purchase as a basis for comparing prices between stores. It may also be valuable to relate similar items to understand where cost savings could come from substitute products, e.g. different types of apples
5. Graphical breakdowns, such as pie charts and drill-downs, to help make sense of data; trend visualizations and graphical comparisons


Future:
1. Learning from previous receipts to categorize new line-items
2. Learning from existing data to understand a suitable default unit for new products that are added. Example: Produce is typically measured in pounds, so new produce would start from a default of 1lb units.
3. Improved parsing based on insights (ML?) from different stores. What do I mean by this???
4. Background processing that tries to identify potential cost savings and alerts user for what's found
5. Client-side optimizations, such as image pre-processing, maybe even EasyOCR processing as well, if possible, then send all to server for archival
    5.a. Consider what's required to secure any EasyOCR training from being reverse-engineered or taken?
6. Additional EasyOCR, etc. training to refine process