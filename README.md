# Elasticsearch Movie Plots

To begin the project, I first needed to get hold of Elasticsearch and Kibana. 

I downloaded Elasticsearch 7.11.0 and Kibana 7.11.0, both of which caused security issues with MacOS and I had to allow them both to be run from System Preferences. pandas also had to be installed in the environment. 

## Indexing

To obtain the dataset, I first went to [Kaggle](https://www.kaggle.com/) and created an account. I was then able to access [Wikipedia Movie Plots](https://www.kaggle.com/jrobischon/wikipedia-movie-plots?select=wiki_movie_plots_deduped.csv) to download the `.csv` to be able to use it. Due to the file being quite large, a smaller sample size of 1000 samples were used. In order to upload 1000 samples for indexing, I decided to export the `wiki_movie_plots_duped.csv` file onto a new file with only 1000 samples.

Using the pandas package, it was possible to read through the first 1000 samples by using `iloc`. `iloc[:1000]` returns us the first 1000 rows due to the way slicing notation works with Python. To limit things to 1000 samples, something like `iloc[400:1400]` could be used but I decided to just use `iloc[:sample_size]` instead to keep things simple. `sample_size` is a variable that contains the [integer 1000](https://github.com/sachinlim/elasticsearch-movie-plots/blob/main/elasticsearch.py#L29) and we are getting the first 1000 samples, in this case.

After I had Python return 1000 samples, I made it export to a new external `.csv` file which would be uploaded by using `helpers.bulk()`. The file is labeled as [sample.csv](sample.csv). Unfortunately, GitHub cannot display the file but the data looks like this: 

![image](https://user-images.githubusercontent.com/80691974/210362544-6ab650db-2de5-49f4-aa19-2ee5b373f305.png)


## Sentence Splitting, Tokenization and Normalization

In order to tokenize the text that is being input, I started off by creating a custom analyzer. One of the things I wanted to do for this step was to convert all of the text to lowercase to avoid any issues with words that may have capital letters. From my previous experiences, the words “Dog” and “dog” may not appear to be identified as the same due to the capital D.

Before I could begin converting tokens to lowercase, I had received a few errors throughout the process of making the custom analyzer. When reading the error message, it said that settings could not be updated for “open indices”. After reading the error message, I decided to close the index (`indices.close()` was used) and run the program again, and it worked.

`splitter()` contains the token filters for the search.

![image](https://user-images.githubusercontent.com/80691974/210360534-7218d0ac-65bc-4cce-baee-a4ee36709058.png)

## Searching 

To search through the uploaded index, I had to update the mapper, which I was not doing at first. I was not getting enough results or sometimes there would be no results altogether. I decided to create a `mapping()` that would add the mappings separately. The type for `Release Year` had to be changed to `text` because it was no longer accepting `integer`.


<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/210361143-f72eb74a-2e3f-428b-9788-51825bc1c376.png" width="300">
</p>

To search through the uploaded index, I had to update the mapper, which I was not doing at first. I was not getting enough results or sometimes there would be no results altogether. I decided to create a `mapping()` that would add the mappings separately. 

Queries can be entered in the following format: 
```
GET test73/_search
{
  "query": {
    "match": {
      "Title": "testing kings"
    }
  } 
}

```

Which presents the following: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/210361963-63a5399a-53e6-4b79-96cf-3c1d2bc8ab85.png" width="400">
</p>


