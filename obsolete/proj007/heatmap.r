{\rtf1\ansi\ansicpg1252\deff0\deflang2057{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Msftedit 5.41.21.2510;}\viewkind4\uc1\pard\sa200\sl276\slmult1\lang9\f0\fs22 #http://enotacoes.wordpress.com/2007/11/16/easy-guide-to-drawing-heat-maps-to-pdf-with-r-with-color-key/\par
\par
library(RColorBrewer)\par
library(gplots)\par
x=read.table("matrix.dat", header=TRUE)\par
mat=data.matrix(x)\par
\par
pdf("heatmap2.pdf", height=10, width=10)\par
heatmap.2(mat,\par
Rowv=TRUE,\par
Colv=TRUE,\par
#    dendrogram= c("none"),\par
distfun = dist,\par
hclustfun = hclust,\par
xlab = "X data", ylab = "Y data",\par
key=TRUE,\par
keysize=1,\par
trace="none",\par
density.info=c("none"),\par
margins=c(10, 8),\par
col=rev(brewer.pal(10,"PiYG"))\par
#    col=redgreen(75),\par
)\par
dev.off()\par
}
 