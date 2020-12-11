import { Octokit } from "@octokit/core";

const octokit = new Octokit({
  auth: process.env.RUNEQL_DATA_PUSH,
});

let res = await octokit.request("POST /repos/{owner}/{repo}/pulls", {
  owner: "schmidlidev",
  repo: "runeql-data",
  head: "update",
  base: "main",
  title: "OSRSBOX Data Update",
});

console.log(res);
