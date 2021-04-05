1. IMAGES

    ProductImages Notes from  https://stackoverflow.com/questions/35363982/what-is-the-best-way-to-store-list-of-links-to-cloud-files-in-django-model
    
    The question is are you going to handle the uploads of those images?
    
    If yes, then you'll have to create custom storage system (or use 3rd party one, there're serveral for S3) and then
    use a separate model for images with ImageField, which will store the paths, and link it via many-to-many to your
    main model.
    
    If no, which means you'll just need to return links to the images, then one solution is to use a separate model for
    images with URLFields, which will store the images' URLs, and link it via many-to-many to your main model. Or if
    the images don't repeat between records in main model, and there're a few of them correspond to each record,
    then denormalization would work granting performance boost - use a field on main model to store a list of strings.
    JSONField sounds nice as JSON perfect to store a list of strings, but it's specific for PostgreSQL. But if the list
    of strings is in fact the list of URLs, that won't contain spaces, then the easy way is to just text_filed_value="
    ".join(list_of_strings) them and store in common TextField on the main model and then
    list_of_strings=text_field_value.split(" ") to get them back as list of strings.
   
2. AUTHENTICAION
    JWT - token
   
3. PRODUCT CATEGORY / FITERING
    