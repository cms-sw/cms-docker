# -*- tab-width: 4 -*-
###############################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
###############################################

=head1 Lang module

This module contains the API to language processing.
It is responsible for creating the parser and handling the specific
categories editing.

A language parser is an I<object> with associated methods.
I<Lang.pm> creates the base object, to be augmented/overriden by
specific parsers in directory I<Lang>.
The methods described below are generally only dummy declarations
to capture missing specific implementations.

=cut

package LXR::Lang;

use strict;
use LXR::Common;
use IO::Handle;


=head2 C<new ($writeDB, $pathname, $releaseid, @itag)>

Method C<new> creates a new language object.

=over

=item 1

C<$writeDB>

a I<boolean> I<integer> requesting to write language properties
into the tree database,
passed unaltered to the specific parser initialisation method
(set to 1 only by I<genxref>)

=item 2

C<$pathname>

a I<string> containing the name of the file to parse

=item 3

C<$releaseid>

a I<string> containing the release (version) of the file to parse

B<Note:>

=over

=item

I<Considering all call locations,
this argument is not really necessary and we could as well
use the global variable.>

=back

=item 4

C<@itag>

an I<array> of 3 elements used to generate an C<E<lt> A E<gt>> link
for the identifiers found in the file (just insert the identifier name
between the array elements)

=back

Creation of a specific parser is attempted first based on the file name
and information from configuration parameter C<'filetype'>.
If the file type is unknown,
the first line of the file is read to tentatively extract a I<shebang>
processed through configuration parameter C<'interpreters'>.
In case there is no I<shebang>,
an emacs-style C<mode:> is looked for.

If all fail, C<undef> is returned.

The LXR language name and argument C<@itag> are recorded in
the created parser which is then returned.

=cut

sub new {
	my ($self, $writeDB, $pathname, $releaseid, @itag) = @_;
	my ($lang, $langkey, $type);

	# Try first to find a handler based on the file name
	# (usually only its extension)
	foreach my $lk (keys %{ $config->{'filetype'} }) {
		$type = $config->{'filetype'}{$lk};
		if ($pathname =~ m/$$type[1]/) {
			eval "require $$type[2]";
			die "Unable to load $$type[2] Lang class, $@" if $@;
			my $create = $$type[2] . '->new($writeDB, $pathname, $releaseid, $$type[0])';
			$lang = eval($create);
			die "Unable to create $$type[2] Lang object, $@" unless defined $lang;
			$langkey = $lk;
			last;
		}
	}

	# If it did not succeed, read the first line and try for an interpreter
	if (!defined $lang) {
		my $extract;
		my $fh = $files->getrawfilehandle($pathname, $releaseid);
		return undef if !defined $fh;
		read ($fh, $extract, 1024);
		return undef if &{$config->{'&discard'}}($extract);

		# Try to see if it's a #! script or an emacs mode-tagged file
		($extract =~ m/^\#!\s*(\S+)/s)
		|| ($extract =~ m/^.*-[*]-.*?[ \t;]mode:[ \t]*(\w+).*-[*]-/);

		my $shebang  = $1;
		my %filetype = %{ $config->{'filetype'} };
		my %inter    = %{ $config->{'interpreters'} };

		foreach my $patt (keys %inter) {
			if ($shebang =~ m/${patt}$/) {
				$langkey = $inter{$patt};
				eval "require $filetype{$langkey}[2]";
				die "Unable to load $filetype{$langkey}[2] Lang class, $@" if $@;
				my $create = $filetype{$langkey}[2]
				  . '->new($writeDB, $pathname, $releaseid, $filetype{$langkey}[0])';
				$lang = eval($create);
				last if defined $lang;
				die "Unable to create $filetype{$langkey}[2] Lang object, $@";
			}
		}
	}

	# No match for this file
	return undef if !defined $lang;

	$$lang{'itag'} = \@itag if $lang;
	$$lang{'ltype'} = $langkey;

	return $lang;
}


=head2 C<parseable ($pathname, $releaseid)>

Function C<parseable> returns 1 if the designated file can be parsed
some way or other.

=over

=item 1

C<$pathname>

a I<string> containing the name of the file to parse

=item 2

C<$releaseid>

the release (or version) in which C<$pathname> is expected to
be found

=back

This a streamlined version of method C<new> where the filename argument
is checked against the patterns from I<filetype.conf>
or the first line of the file against the I<interpreters> list.

=cut

sub parseable {
	my ($pathname, $releaseid) = @_;
	my ($lang, $langkey, $type);

	# Try first to find a handler based on the file name
	# (usually only its extension)
	foreach my $lk (keys %{ $config->{'filetype'} }) {
		$type = $config->{'filetype'}{$lk};
		if ($pathname =~ m/$$type[1]/) {
			return 1;
		}
	}

	# If it did not succeed, read the first line and try for an interpreter
	# Try to see if it's a #! script or an emacs mode-tagged file
	my $extract;
	my $fh = $files->getrawfilehandle($pathname, $releaseid);
	return undef if !defined $fh;
	read ($fh, $extract, 1024);
	return undef if &{$config->{'&discard'}}($extract);
	($extract =~ m/^\#!\s*(\S+)/s)
	|| ($extract =~ m/^.*-[*]-.*?[ \t;]mode:[ \t]*(\w+).*-[*]-/);

	my $shebang  = $1;
	my %inter    = %{ $config->{'interpreters'} };
	foreach my $patt (keys %inter) {
		if ($shebang =~ m/${patt}$/) {
			return 1;
		}
	}

	# No match for this file
	return undef;
}


=head2 C<multilinetwist ($frag, $css)>

Internal function C<multilinetwist> marks the fragment with a CSS class.

=over

=item 1

C<$frag>

a I<string> to mark

=item 2

C<$css>

a I<string> containing the CSS class

=back

The fragment is surrounded with C<E<lt> SPAN E<gt>> and C<E<lt> /SPAN E<gt>>
tags. Special care is taken to repeat these tags at end of lines, so
that the fragment can be correctly displayed on several lines without
disturbing other highlighting (such as line numbers or difference marks).

=cut

sub multilinetwist {
	my ($frag, $css) = @_;
	$$frag = "<span class=\"$css\">$$frag</span>";
	$$frag =~ s!\n!</span>\n<span class="$css">!g;
	$$frag =~ s!<span class=".+?"></span>$!!; #remove excess marking
}


=head2 C<processcomment ($frag)>

Method C<processcomment> marks the fragment as a comment.

=over

=item 1

C<$frag>

a I<string> to mark

=back

Uses function C<multilinetwist>.

=cut

sub processcomment {
	shift @_;
	goto &multilinetwist;
}


=head2 C<processstring ($frag)>

Method C<processstring> marks the fragment as a string.

=over

=item 1

C<$frag>

a I<string> to mark

=back

Uses function C<multilinetwist>.

=cut

sub processstring {
	shift @_;
	goto &multilinetwist;
}


=head2 C<processextra ($frag, $kind)>

Method C<processextra> marks the fragment as language specific.

=over

=item 1

C<$frag>

a I<string> to mark

=item 2

C<$kind>

a I<string> containing the CSS class

=back

Uses function C<multilinetwist>.

=cut

sub processextra {
	shift @_;
	goto &multilinetwist;
}

#
# Stub implementations of this interface
#


=head2 C<processinclude ($frag, $dir)>

Method C<processinclude> is invoked to process an I<include> directive.

=over

=item 1

C<$frag>

a I<string> containing the directive

=item 2

C<$dir>

an optional I<string> containing a preferred directory for the include'd file

=back

Usually, the link to the include'd file is built with C<'incref'>.
Consequently, the directories in C<'incprefix'> are also searched.

=cut

sub processinclude {
	my ($self, $frag, $dir) = @_;
	warn  __PACKAGE__."::processinclude not implemented. Parameters @_";
	return;
}


=head2 C<_linkincludedirs ($link, $file, $path, $dir)>

Internal function C<_linkincludedirs> builds links for partial paths in C<$link>.

=over

=item 1

C<$link>

a I<string> containing an already processed link,
i.e. the result of an invocation of C<incref> or C<incdirref>.

=item 2

C<$file>

a I<string> containing the target file name in the language-specific
dialect (without language-specific separator replacement),

=item 3

C<$sep>

a I<string> containing the language-specific path separator,

=item 4

C<$path>

a I<string> containing the target file name as an OS file name
(path separator is /),

=item 5

C<$dir>

a I<string> containing the last directory argument for C<incdirref>.

=back

This function is a utility function reserved for the language parsers.

=cut

sub _linkincludedirs {
	my ($self, $link, $file, $sep, $path, $dir) = @_;
	my ($sp, $l, $r);	# various separator positions
	my $tail;

	if	(	!defined($link)
		&& index($path, '/') < 0
		) {
			$tail = $file;
	} elsif (substr($path, -1) eq '/') {
		# Path ends with /: it may be a directory or an HTTP request.
		# Remove trailing / and do an initial processing.
		chop($path);
		$tail = '';
		# Protect against erroneous multiple separators
		while (substr($path, -1) eq '/') {
			chop($path);
			$tail .= $sep;
			$file = substr($file, 0, rindex($file, $sep));
		};
		$link = incdirref($file, 'include', $path, $dir);
	}
	# If incref or incdirref did not return a link to the file,
	# explore however the path to see if directories are
	# known along the way.
	while	(	index($path, '/') >= 0
			&&	substr($link, 0, 1) ne '<'
			) {
		# NOTE: the following rindex never returns -1, because
		#		we test for the presence of a separator before
		#		iterating the loop.
		$sp = rindex ($file, $sep);
		$tail = substr($file, $sp) . $tail;
		$file = substr($file, 0, $sp);
		$path =~ s!/[^/]+$!!;
		# Protect against erroneous multiple separators
		while (substr($path, -1) eq '/') {
			chop($path);
			$tail = $sep . $tail;
			$file = substr($file, 0, rindex($file, $sep));
		};
		$link = incdirref($file, 'include', $path, $dir);
	}
	# A known directory (at least) has been found.
	# Build links to higher path elements
	if (substr($link, 0, 1) eq '<') {
		while (index($path, '/') >= 0) {
			# NOTE: see note above about rindex
			$l = index  ($link, '>');
			$r = rindex ($link, '<');
			$sp = rindex (substr($link, 1+$l, $r-$l-1), $sep);
			substr($link, 1+$l, $sp+length($sep)) = '';
# 			$link =~ s!^([^>]+>)([^/]*/)+?([^/<]+<)!$1$3!;
			$tail = $sep . $link . $tail;
			$sp = rindex ($file, $sep);
			$file = substr($file, 0, $sp);
			$path =~ s!/[^/]+$!!;
		# Protect against erroneous multiple separators
			while (substr($path, -1) eq '/') {
				chop($path);
				$tail = $sep . $tail;
				$file = substr($file, 0, rindex($file, $sep));
			};
			$link = incdirref($file, 'include', $path, $dir);
		}
	}
	return $link . $tail;
}


=head2 C<_incfindfile ($filewanted, $file, @paths)>

Function C<_incfindfile> returns the "full" path corresponding to argument
C<$file>.

=over

=item 1

C<$filewanted>

a I<flag> indicating if a directory (0) or file (1) is desired

=item 2

C<$file>

a I<string> containing a file name to resolve

=item 3

C<@paths>

an I<array> containing a list of directories to search

=back

The list of directories from configuration parameter C<'incprefix'> is
appended to C<@paths>. Every directory from this array is then preprended
to the file name . The resulting string is transformed by the mapping
rules of configuration parameter C<'maps'> (See I<Config.pm> sub C<mappath>).

If there is a match in the file database (file or directory according
to the first argument), the "physical" path is returned.
Otherwise, an C<undef> is returned to signal an unknown file.

I<This is a "private" or "internal" C<sub> for include path resolution only.>

=cut

sub _incfindfile {
	my ($filewanted, $file, @paths) = @_;
	my $path;

	# The following line could be faster interpreted as
	# 	push(@paths, @{$config->{'incprefix'}});
	# but this would forbid variable expansion.
	# Is this feature really needed for include path?
	push(@paths, $config->incprefix);

	foreach my $dir (@paths) {
		$dir =~ s!/+$!!;	# Remove trailing slashes
		$path = $config->mappath($dir . '/' . $file);
		if ($filewanted){
			return $path if $files->isfile($path, $releaseid);
		} else {
			return $path if $files->isdir($path, $releaseid);
		}
	}

	return undef;
}


=head2 C<incdirref ($name, $css, $file, @paths)>

Function C<incdirref> returns an C<E<lt> A E<gt>> link to a directory
of an C<include>d file or the directory name if it is unknown.

=over

=item 1

C<$name>

a I<string> for the user-visible part of the link,
usually the directory name

=item 2

C<$css>

a I<string> containing the CSS class for the link

=item 3

C<$file>

a I<string> containing the HTML path to the directory

=item 4

C<@paths>

an I<array> containing a list of base directories to search

=back

I<This function is supposed to be called AFTER sub C<incref> on every
subpath of the include'd file, removing successively the tail directory.
It thus allows to compose a path where each directory is separately
clickable.>

If the include'd directory does not exist (as determined by sub C<incfindfile>),
the function returns the directory name. This acts as a "no-op" in the
HTML sequence representing the full path of the include'd file.

If the directory exists, the function returns the C<E<lt> A E<gt>> link
as computed by sub C<fileref> for the directory.

=cut

sub incdirref {
	my ($name, $css, $file, @paths) = @_;
	my $path;

	$path = _incfindfile(0, $file, @paths);
	return $name unless $path;
	return &fileref	( $name
					, $css
					, $path.'/'
					);
}


=head2 C<processcode ($code)>

Method C<processcode> processes the fragment as code.

=over

=item 1

C<$code>

a I<string> to mark

=back

=cut

sub processcode {
	my ($self, $code) = @_;
	warn  __PACKAGE__."::processcode not implemented. Parameters @_";
	return;
}


=head2 C<processreserved ($frag)>

Method C<processreserved> marks the fragment as a reserved word.

=over

=item 1

C<$code>

a I<string> to mark

=back

B<Note:>

=over

=item

I<This method is nowhere invoked because keywords are processed in
C<processcode> simultaneouly with identifiers.
It corresponds to no category. It is
thus candidate for removal.>

=back

=cut

sub processreserved {
	my ($self, $frag) = @_;
	warn  __PACKAGE__."::processreserved not implemented. Parameters @_";
	return;
}


=head2 C<indexfile ($name, $path, $fileid, $index, $config)>

Method C<indexfile> is invoked during I<genxref> to parse and collect
the definitions in a file.

=over

=item 1

C<$name>

a I<string> containing the LXR file name

=item 2

C<$path>

a I<string> containing the OS file name

When files are stored in VCSes, C<$path> is the name of a temporary file.

=item 3

C<$fileid>

an I<integer> containing the internal DB id for the file/revision

=item 4

C<$index>

a I<reference> to the index (DB) object

=item 5

C<$config>

a I<reference> to the configuration objet

=back

=cut

sub indexfile {
	my ($self, $name, $path, $fileid, $index, $config) = @_;
	warn  __PACKAGE__."::indexfile not implemented. Parameters @_";
	return;
}


=head2 C<referencefile ($name, $path, $fileid, $index, $config)>

Method C<referencefile> is invoked during I<genxref> to parse and collect
the references in a file.

=over

=item 1

C<$name>

a I<string> containing the LXR file name

=item 2

C<$path>

a I<string> containing the OS file name

When files are stored in VCSes, C<$path> is the name of a temporary file.

=item 3

C<$fileid>

an I<integer> containing the internal DB id for the file/revision

=item 4

C<$index>

a I<reference> to the index (DB) object

=item 5

C<$config>

a I<reference> to the configuration objet

=back

=cut

sub referencefile {
	my ($self, $name, $path, $fileid, $index, $config) = @_;
	warn  __PACKAGE__."::referencefile not implemented. Parameters @_";
	return;
}


=head2 C<language ()>

Method C<language> is usually a shorthand notation for
C<$lang-E<gt>{'language'}>.

=cut

sub language {
	my ($self) = @_;
	my $languageName;
	warn  __PACKAGE__."::language not implemented. Parameters @_";
	return $languageName;
}

1;
