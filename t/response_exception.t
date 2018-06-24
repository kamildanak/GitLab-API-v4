#!/usr/bin/env perl
use strictures 2;

{
    package Test::FakeRESTClient;
    use Moo;
    extends 'GitLab::API::v4::RESTClient';
    sub _http_tiny_request {
        return {
            success => 0,
            status  => 500,
            reason  => 'Internal Server Error',
        };
    }
}

use Test2::V0;
use GitLab::API::v4;
use GitLab::API::v4::ResponseException;
use Try::Tiny;

my $api = GitLab::API::v4->new(
    url               => 'https://example.com/api/v4',
    rest_client_class => 'Test::FakeRESTClient',
);

my $error;
try { $api->users() }
catch { $error = $_ };

is(
    "$error",
    'Error GETing https://example.com/api/v4/users (HTTP 500): Internal Server Error',
    'message matches expectations',
);

ok(
    (! $api->is_response_exception(undef) ),
    'undef is not a response exception object',
);

ok(
    (! $api->is_response_exception('foo') ),
    '"foo" is not a response exception object',
);

{ package Test::FooObject; use Moo }
ok(
    (! $api->is_response_exception( Test::FooObject->new() ) ),
    'random object is not a response exception object',
);

ok(
    $api->is_response_exception($error),
    'a response exception object looks like one',
);

done_testing;
