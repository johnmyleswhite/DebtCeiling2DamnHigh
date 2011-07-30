library('lubridate')

urls <- read.csv('urls.tsv', header = FALSE, sep = '\t', stringsAsFactors = FALSE)
names(urls) <- c('URL', 'HTMLMatches', 'URLMatches')

clicks <- read.csv('clicks.tsv', header = FALSE, sep = '\t', stringsAsFactors = FALSE)
names(clicks) <- c('URL', 'HC', 'T')

html.stats <- with(urls, mean(HTMLMatches, na.rm = TRUE))
url.stats <- with(urls, mean(URLMatches, na.rm = TRUE))

click.data <- merge(urls, clicks, by = 'URL')

# Within a time window, compute proportion of clicks related to Debt Ceiling.
unix2POSIXct  <-  function (time)
{
  structure(time, class = c("POSIXt", "POSIXct"))
}

click.data <- transform(click.data, HC = unix2POSIXct(HC))
click.data <- transform(click.data, T = unix2POSIXct(T))

write.csv(click.data, file = 'click_data.csv', row.names = FALSE)

click.data <- click.data[order(click.data$T), ]

window <- 200

window.data <- data.frame()

for (i in 0:(nrow(click.data) %/% window))
{
  local.data <- click.data[(i * window + 1):((i + 1) * window), ]
  html.stats <- with(local.data, mean(HTMLMatches, na.rm = TRUE))
  url.stats <- with(local.data, mean(URLMatches, na.rm = TRUE))
  window.data <- rbind(window.data, data.frame(Time = with(local.data, median(T, na.rm = TRUE)), HTMLMatches = html.stats, URLMatches = url.stats))
}

# Want windows of 15 minutes.
max.time <- with(click.data, max(T, na.rm = TRUE))
min.time <- with(click.data, min(T, na.rm = TRUE))

top.time <- max.time

window.data <- data.frame()

while (top.time > min.time)
{
  local.data <- subset(click.data, T < top.time & T > top.time - new_duration(minute = 5))
  html.stats <- with(local.data, mean(HTMLMatches, na.rm = TRUE))
  url.stats <- with(local.data, mean(URLMatches, na.rm = TRUE))
  window.data <- rbind(window.data, data.frame(Time = top.time, HTMLMatches = html.stats, URLMatches = url.stats))
  top.time <- top.time - new_duration(minute = 5)
}

time.series <- melt(window.data, id.vars = 'Time')

names(time.series) <- c('Time', 'Type', 'Matches')
levels(time.series$Type) <- c('Website mentions Debt', 'URL contains Debt')

p <- ggplot(time.series, aes(x = Time, y = Matches, color = Type)) +
  geom_line() +
  ylim(0, 1) +
  ylab('Percentage of All 1.usa.gov Links') +
  opts(title = 'The Debt Ceiling is Too Damn High') +
  opts(legend.position = 'none')
ggsave('links.pdf')

