---
title: "quickdraw"
author: "Ying Ji"
date: "November 3, 2018"
output: html_document
---



library(dplyr)
library(ggplot2)
draw$drawing<-NULL
draw$key_id<-NULL
ct<-(table(draw$countrycode)/nrow(draw)*100) %>% sort %>% tail(20) %>% as.data.frame()
ggplot(data=ct,aes(x=Var1,y=Freq))+geom_bar(stat="identity",fill="steelblue")+theme(axis.text.x = element_text(angle = 45, hjust = 1))+xlab("country")+ylab("percentage")

truepro<-draw%>% group_by(word) %>% filter(recognized=="True") %>% summarise(n=n()/500) %>% as.data.frame()

#animal
sum(unique(draw$word) %in% tolower(anilib[,1]))

aniname<-unique(draw$word) %in% tolower(anilib[,1])
anilist<-unique(draw$word)[aniname]

## Including Plots

You can also embed plots, for example:

```{r pressure, echo=FALSE}
plot(pressure)
```

Note that the `echo = FALSE` parameter was added to the code chunk to prevent printing of the R code that generated the plot.
