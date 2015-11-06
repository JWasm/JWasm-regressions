use File::Temp qw/ tempfile tempdir /;

# usage: cat sf-bugs.txt | perl run.pl
# usage: cat sf-features.txt | perl run.pl

while ($line = <STDIN>) {
	chomp($line);
	($fh, $filename) = tempfile();
	print $fh $line;
	close $fh;
	my $action = sprintf("http_proxy= curl -X POST -u \"milabs:<PASSWORD>\" -i -d @%s https://api.github.com/repos/jwasm/jwasm/issues", $filename);
	system($action);
	sleep(1); # prevent from blocking by github
}
