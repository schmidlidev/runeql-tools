import { Octokit } from "@octokit/core";

const octokit = new Octokit({
  auth: process.env.RUNEQL_BOT_KEY,
});

// Create PR
let res = await octokit.request("POST /repos/{owner}/{repo}/pulls", {
  owner: "schmidlidev",
  repo: "runeql-data",
  head: "update",
  base: "main",
  title: "OSRSBOX Data Update",
});
console.log(res);
let prNumber = res.data.number;

// Request PR review
res = await octokit.request(
  "POST /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers",
  {
    owner: "schmidlidev",
    repo: "runeql-data",
    pull_number: prNumber,
    reviewers: ["schmidlidev"],
  }
);
console.log(res);
