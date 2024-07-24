# Programming Project 02: Reproducing and extending DNS research

## Overview
In this project, you will reproduce and extend some of the measurements in the networking research paper "[Measuring the Consolidation of DNS and Web Hosting Providers
](https://arxiv.org/pdf/2110.15345.pdf)."

The instructions are **deliberately underspecified** to help prepare you for conducting your own research project during the second half of the semester. You have developed an extensive array of problem solving, documentation reading, and testing and debugging skills throughout the computer science courses you have taken at Colgate. This project is an opportunity to showcase your computer science prowess.

### Learning objectives
After completing this project, you should be able to:
* Design simple network measurement experiments based on experimental designs described in a research paper
* Combine multiple types of network observations
* Clearly and concisely present the results of simple measurement experiments

### Important tips
* **Thoroughly read the project instructions and research paper before you conduct any experiments.** Research shows "that the ['new norm' in reading is _skimming_](https://www.theguardian.com/commentisfree/2018/aug/25/skim-reading-new-normal-maryanne-wolf), with word-spotting and browsing through the text. [...] When the reading brain skims like this, [...] we don’t have time to grasp complexity."
* **Start the project shortly after it is released and work on the project over multiple sessions.** This will give you time to think about how to solve problems, allow you to ask questions, and result in better outcomes. The opportunity to revise your project is contingent upon your git commit history demonstrating that you started the project shortly after it was released and you worked on the project over multiple sessions.
* **Follow network measurement best practices.** This will help prevent your measurements from interfering with the normal operation of DNS servers or other network infrastructure. In particular,
    * **Test your code on a small scale** before conducting large scale experiments—for example, make sure loops in your code work correctly, such that you do not unintentionally send a large volume of requests due to infinite or other overly aggressive looping
    * **Use the caching recursive resolver explicitly set up for this project** to avoid issuing excessive requests to external DNS servers

## Objective
Your goal is to reproduce and extend the results presented in the first two paragraphs of Section 4.1 in the paper "[Measuring the Consolidation of DNS and Web Hosting Providers
](https://arxiv.org/pdf/2110.15345.pdf)." In particular, you must:
* Identify the percentages of domains in the Tranco Top 10K that exclusively use one AS organization to host their name servers (Table 1)
* Identify the percentages of domains in the Tranco Top 10K whose name servers are exclusively in-bailiwick (a new result not presented in the paper)

You should use the same methodology as the paper with a few minor variations:
* Use the latest [Tranco list](https://tranco-list.eu/), not the September 2022 snapshot used in the paper
* Conduct a DNS lookup, instead of querying a whois server, to determine a domain's name servers
* Use the DNS interface, instead of the whois interface, for [Team Cymru's IP to ASN Mapping Service](https://www.team-cymru.com/ip-asn-mapping)

## Suggestions
Write one or more Python programs that use [dnspython](http://www.dnspython.org/) to conduct DNS lookups. You should issue queries to the local recursive resolver that has been set up for this project: `127.0.0.1`, port `8053`. Here is an example:

```Python
import dns.resolver
r = dns.resolver.Resolver()
r.nameservers = ['127.0.0.1']
r.port = 8053
result = r.resolve("portal.colgate.edu", "A")
for data in result:
    print(data)
```

When you are running your program(s) for 10K domains, you should run it using [screen](https://linuxize.com/post/how-to-use-linux-screen/). This will ensure your script will keep running on the server, even if your SSH session is terminated. As noted above, make sure you test your program with a small number of domains (e.g., 50), before you run it on all 10k.

You should conduct the measurements in stages. Write a separate program for each stage that takes the results from the previous stage as input and outputs the results from the current stage.

You should practice defensive programming. In other words, make sure your program(s) handle failures (e.g., bad DNS response, no DNS response, etc.) gracefully and do not crash. This will help ensure that your script doesn’t crash halfway through the 10k domains.

## Submission instructions
Create a `results.md` file (use proper [markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)) that includes:
1. Instructions for duplicating your experiments: e.g., what Python program(s) should be run? What parameters do they take? Do any other programs/shell commands need to be run?
2. Your version of Table 1 and a short paragraph explaining it (similar to the second paragraph in Section 4.1 of the paper)
3. A paragraph describing your methodology for determining if a domain's name servers are exclusively in-bailiwick, and a short paragraph describing the results of this analysis

Your repository should include:
1. Your `results.md`
2. Any Python program(s) you have written to conduct the experiments
3. Any raw data resulting from your experiments# Reproducing-DNS-Research-Project
"# Reproducing-DNS-Research-Project" 
# Reproducing-DNS-Research-Project
