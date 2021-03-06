library(httr)
library(jsonlite)
source("config.R")

#Reading the initial CSV in a data frame object and adding some blank fields
table <- read.csv(file=initial_file_path, header=TRUE, sep=",", stringsAsFactors = FALSE)
new_columns <- c("Genre", "IMDBRating", "IMDBVotes", "Director", "RottenTomatoesRating", "Production")
for (i in new_columns){
  table[,i] <- NA
}

# This is a counter of the movies we find.
# We only want to get data on 2000 movies 
found_movies <- 0

# We iterate through the movies and get extra data from the OMDB API
for (i in 1:NROW(table)){
  title <- table[i, 1]
  print(title)
  response <- GET("http://www.omdbapi.com/?",
           query = list("apikey" = "863c5282", "t" = title)
  )
#<<<<<<< #HEAD:Assignment1/script1.R
  #if (content(response)$Response){ #BOGDAN IF
#=======

#>>>>>>># 0dbea5d2d7eb43d1666d3acd62ab86e425fd7e80:Assignment1/enrich_script.R
  if (is.null(content(response)$Response) == FALSE){
    found_movies <- found_movies + 1
    print(found_movies)
    #TengXu94: I need this if check movie 21 does not have the Genre field -> replacement has length zero error!
    if (length(content(response)$Genre) > 0){
      table[i,6] <- content(response)$Genre
    }
    if (length(content(response)$Ratings) > 0){
      table[i,7] <- content(response)$Ratings[[1]]$Value
      if (length(content(response)$Ratings)>1){
        table[i,10] <- content(response)$Ratings[[2]]$Value
      }
    }
    #We put if control also here because for some movie they do not have those data
    if (length(content(response)$imdbVotes) > 0){
      table[i,8] <- content(response)$imdbVotes
    }
    if (length(content(response)$Director) > 0){
      table[i,9] <- content(response)$Director
    }
    
    # If the revenue info is empty, then we replace it with the revenue info from
    # OMDB API
    if (table[i,5] == 0){
      if (identical(content(response)$BoxOffice,"N/A" == FALSE)){
        table[i,5] <- content(response)$BoxOffice
      }
    }
    
    #Same for release date!
    if (length(content(response)$Released)>0 && content(response)$Released != "N/A"){
      table[i,2] <- content(response)$Released
    }
    if (length(content(response)$Production)>0){
      print(content(response)$Production)
      table[i,11] <- content(response)$Production
    }
  }
  if (found_movies > 2999){
    break;
  }
}

# Save the enriched data in a new list
write.csv(file=enriched_file_path, x=table)
