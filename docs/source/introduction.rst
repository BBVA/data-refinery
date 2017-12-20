Introduction
============

Motivation
----------
Data Analytics is now very popular on modern companies. Nowadays nobody deny the data insights value regarding business development. Also technology allow us to manage huge amount of data, even when look imposible to process. In fact, scientific libraries allow us to perform advaced analytics.

> But i can't stop thinking about move local work to the cluster, and for me looks like a lonely valley.

This work is a must every time that a hypothesis looks promising and must hit the real world. Doing this job it's like walk along a lonely valley plenty of obstacles. The scientific libraries usually are not desingned to scale beyond machine memory (usually this is a very hard task) because modern machines are big enought. But a lot of times I spent time translating from R o Python to Java or Scala; just because clusters software is tipically programed on JVM languages.

I think that smaller the transformation code, the better is translation to the cluster software. And also Python nowadays live between the two worlds.

Solutions
---------
I usually talk about this translation problem with my colleagues on Big Data events. Some of then put cluster tools in hands of their data scientist, like Spark. But this comes with a cost, every test boot up a complete cluster on the local machine, slow down the development process. But not every test must hit the real work, so comes with an unnecesary adaptation to the cluster, instead a quick local test. Also there is an slightly outdated AI algorithms on cluster libraries.
Some times people try to do the work directly on real cluster, with real data. Thats awesome but await to all the data be processed, usually slow down development process.

There is no silver bullet for this problem, every solution that you try has its own tradeoffs. Like "i must develop on cluster, but every test run for days" or like "i have my program finished but i must rewrite it in java"

On my opinion the only way to go is more automation and be iterative, so the scientific can use their own tools and the engineer can work less. When we say iterative it's not only about development, it's also about use more data if our hypotesis is still alive. Automation allow us to be more productive and secure.

>  Automation reveals the importance of a good data pipeline.

Help not substitution
---------------------
If we want to be successful we need steal the better of other tools, not try to reinvent the wheel. Big Data framework move data from one place to another very well, and also can distribute computation easilly.

> But when we want add a field, or split a date field, it's completely on our hands.

Scientific libraries, also, help us loading data and show information, but if we want do a transformation, again it's in our hands.

Transformations are the more tedious work. And are written directly on the language of the cluster or notebook. The data refinery library comes to help here, giving you code that runs on cluster or notebook. This library it's not a complete ETL solution, but proves to be a huge help when things going real.

This can be done thanks it's minimalist interface and contained scope. Library only do one thing very well, transform data. It build a function that you can use anywhere. So if you need run a small script, you can use it, or if you need to scale up the process, you can use Spark.

Focus on streaming
------------------

Real world is not static, never stop, so we focus on streaming solutions. Sometimes people ask me "where i config the data file?" or "how i obtain all the values of the column?. On streaming environment you only have two things, a function and the current row. If you have a file, it's your work to split into rows and pass it to the transform function. Streamings are endless so you can't know all the values of a column.

As we say, this library does not do work that other frameworks do better. Pandas and Spark can load files easily and send results elsewhere. I strongly recommend you use a framework where you find confortable, and use this library as help.

Data scientist are usually used to work with Pandas. Its interface is based on columns, very efficient on batch, but not on streaming. If you are used to Pandas, maybe this approach will twist your mind.

> Work thinking about row not column.

This approach it's resource friendly, and you can use on any machine, you only need one row in memory.
