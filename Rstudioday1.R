print("hi")


getwd()

setwd("C:/ex")

getwd()

read.csv(file.choose())

sampleData<-read.csv(file.choose())

str(sampleData)


#람브스프
lamvf

?summary

summary(sampleData) # 평균등의 값

table(sampleData$성별)

barplot(table(sampleData$성별)) # 통계적, 시각적 자료

summary(sampleData)

boxplot(sampleData$키)

x_bar<-mean(sampleData$키)

x_bar - sampleData$키

sum(x_bar - sampleData$키)

#c : combine 벡터로 만들때/// x,y : 모델을 만들기 위한 훈련 set

x<-c(2,4,6,8)
y<-c(81,93,91,97)

stats::lm()

lm(y~x) # 종속변수 ~ 독립변수
summary(lm(y~x))

height<-c(166,170,168,172,174)
x_bar<-mean(height)

sqrt(((x_bar-height)^2)/length(height))

sqrt(sum((x_bar-height)^2)/length(height))

sqrt(sum((x_bar-height)^2)/4)

sqrt(sum((x_bar-height)^2)/length(height-1))
