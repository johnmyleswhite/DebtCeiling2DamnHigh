stats <- read.csv('matches.tsv', header = FALSE, sep = '\t', stringsAsFactors = FALSE)
names(stats) <- c('URL', 'HTMLMatch', 'URLMatch')

html.stats <- with(stats, mean(HTMLMatch, na.rm = TRUE))
url.stats <- with(stats, mean(URLMatch, na.rm = TRUE))
