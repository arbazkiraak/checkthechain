from ctc import directory
from ctc import evm
from ctc.toolbox import web3_utils


def get_feed_aggregator(*, feed_name=None, feed_address=None):

    if feed_address is None:
        feed_address = directory.chainlink_feeds[feed_name]

    return web3_utils.call_web3_contract(
        contract=feed_address,
        function='aggregator',
    )


def get_feed_data(
    *,
    feed_name=None,
    feed_address=None,
    start_block=None,
    end_block=None,
    normalize=True,
    answer_only=True,
):

    # get feed address
    if feed_address is None:
        feed_address = directory.chainlink_feeds[feed_name]

    # get aggregator
    aggregator_address = web3_utils.call_web3_contract(
        contract=feed_address,
        function='aggregator',
    )

    # parse block
    if end_block is None:
        end_block = 'latest'
    if start_block == 'latest':
        start_block = evm.get_block_number('latest')
    if end_block == 'latest':
        end_block = evm.get_block_number('latest')
    if start_block is None:

        events_list = evm.list_events(
            contract_address=aggregator_address,
            event_name='AnswerUpdated',
        )

        if (
            events_list is not None
            and events_list.get('block_range') is not None
            and len(events_list['block_range']) > 0
        ):
            # use first recorded block
            start_block = events_list['block_range'][0]
        else:
            # use aggregator creation block
            start_block = evm.get_contract_creation_block(
                contract_address=aggregator_address
            )

    # events
    feed_data = evm.get_events(
        event_name='AnswerUpdated',
        contract_address=aggregator_address,
        start_block=start_block,
        end_block=end_block,
    )

    if normalize:
        pass

    if answer_only:
        feed_data = feed_data['arg__current']
        feed_data = feed_data.droplevel('transaction_index')
        feed_data = feed_data.droplevel('log_index')

    return feed_data

