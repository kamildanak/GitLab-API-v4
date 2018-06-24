package GitLab::API::v4::ResponseException;

=head1 NAME

GitLab::API::v4::ResponseException - Exception class for response errors.

=head1 SYNOPSIS

    use GitLab::API::v4;
    use Try::Tiny;

    my $api = GitLab::API::v4->new( ... );

    try {
        $api->some_api_call( ... );
    }
    catch {
        die $_ if !$api->is_response_exception($_);

        print 'ERROR REQUEST CONTENT: ' . $_->req->{content};
        print 'ERROR RESPONSE CONTENT: ' . $_->res->{content};
        die $res->{reason};
    };

=head1 DESCRIPTION

This class is used by L<GitLab::API::v4::RESTClient> to produce exceptions
when a non-successful HTTP response is returned.

=head1 STRINGIFICATION

If objects of this class are stringified then they will return the
L</message>.

=cut

use Types::Standard -types;

use strictures 2;
use namespace::clean;
use Moo;

use overload '""' => sub{ $_[0]->message() };

=head1 ATTRIBUTES

=head2 res

The response hash ref.  Contains the keys C<success>, C<status>,
C<reason>, C<content>, and others.  See L<HTTP::Tiny/request> for
a full list.

=cut

has res => (
    is       => 'ro',
    required => 1,
);

=head2 req

The requet hash ref.  Contains the keys C<method> and C<url>.  May
contain other keys depending on if an C<$options> hash ref was
passed to L<HTTP::Tiny/request>.

=cut

has req => (
    is       => 'ro',
    required => 1,
);

=head2 message

A nicely formatted erorr message.

=cut

has message => (
    is       => 'lazy',
    init_arg => undef,
);
sub _build_message {
    my ($self) = @_;

    my $res = $self->res();
    my $req = $self->req();

    return sprintf(
        'Error %sing %s (HTTP %s): %s',
        $req->{method}, $req->{url},
        $res->{status}, ($res->{reason} || 'Unknown'),
    );
}

1;
__END__

=head1 AUTHORS

See L<GitLab::API::v4/AUTHOR> and L<GitLab::API::v4/CONTRIBUTORS>.

=head1 LICENSE

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

