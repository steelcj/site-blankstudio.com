// The year in the copyright line, resolved when the site is built.
//
// It used to be written by JavaScript on load, which meant a reader with
// scripting off saw "© Vishpala" with a gap where the year should be, and every
// reader saw it appear a moment late. The year is a build-time fact, so the
// build states it.
//
// Read in the site's own publication time zone rather than the build machine's.
// A build that runs at 20:30 in Toronto on 31 December is already the next year
// in UTC, and a copyright line that flips a day early — or late, depending on
// which continent the build ran on — is wrong in a way nobody would think to
// check. This is the same reasoning, and the same declared zone, that
// .eleventy.js uses to keep publication dates from drifting with the builder.

const site = require("./site.json");

module.exports = function () {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: site.publicationTimeZone,
    year: "numeric",
  }).format(new Date());
};
