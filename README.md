# 4Truths

The 4thruths bot posts the front pages of 4 news sites each day. It pulls from a quai-balanced selection of sites using the data from the [ad fontes media interactive bias chart](https://www.adfontesmedia.com/interactive-media-bias-chart/).

### Methodology

The site list is processed in the following ways:

* Remove sites below the recommended quality cutoff of 24
* Remove sites if they won't producr good visual results
* Calculate the median bias for each site
* Calculate the overall median (`Om`) of all sites
* Calculate the median of biases less than `Om` (`Lm`) and greater than or equal to `Om` (`Rm`)
* Divide the sites into 4 buckets `L2`, `L1`, `R1`, and `R2`
* A post pulls a site from each bucket

