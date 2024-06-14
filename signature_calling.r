library(BSgenome.Mmusculus.UCSC.mm10)
library(MutationalPatterns)
library(ggplot2)

genome <- BSgenome.Mmusculus.UCSC.mm10
setwd("filtered")

samples = c("atm1", "atm10", "atm2", "atm3", "atm4", "atm5", "atm6", "atm7", "atm8", "atm9", "wt1", "wt2", "wt4", "wt5", "wt6")
files = list.files()[-20]



print(files[grepl("wt", files)])
print(samples[grepl("wt", samples)])
vcfs <- read_vcfs_as_granges(files[grepl("wt", files)], samples[grepl("wt", samples)], genome, type=c("indel"))
gets <- get_indel_context(vcfs, genome)
counts <- count_indel_contexts(gets)   
plots <- plot_indel_contexts(counts)
#write.csv(counts, paste0("wt_id_sigs.csv"))


plots <- plot_indel_contexts(counts)

ggsave(plots, file="wt_id_sig_test1.png", width = 20, height = 4.5, dpi=500, bg='white')



print(files[grepl("atm", files)])
print(samples[grepl("atm", samples)])
vcfs <- read_vcfs_as_granges(files[grepl("atm", files)], samples[grepl("atm", samples)], genome, type=c("indel"))
gets <- get_indel_context(vcfs, genome)
counts <- count_indel_contexts(gets)   
plots <- plot_indel_contexts(counts)
#write.csv(counts, paste0("atm_id_sigs.csv"))

plots <- plot_indel_contexts(counts)

ggsave(plots, file="atm_id_sig_test1.png", width = 20, height = 8, dpi=500, bg='white')




